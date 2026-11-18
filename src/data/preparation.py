"""Prepare lexical features while preserving the EDA split and source lineage."""
from pathlib import Path
import hashlib
import json
import platform
import importlib.metadata

import numpy as np
import pandas as pd
from src.features import FEATURE_NAMES, SCHEMA_VERSION, extract_url_features, hostname_group


def prepare_rows(raw: pd.DataFrame, manifest: pd.DataFrame) -> dict:
    """Build X/y/metadata, exact-URL representative map and quarantine.

    All source indices are zero-based CSV data row positions. No transform is
    learned from any partition. Failed URL parsing is quarantined with a reason.
    Conflicting targets or split leakage stop the entire run.
    """
    if not raw.index.equals(pd.RangeIndex(len(raw))):
        raise ValueError('Source must use zero-based row positions.')
    if not {'URL', 'label'}.issubset(raw.columns):
        raise ValueError('Source URL and label required.')
    if raw.label.isna().any() or not raw.label.isin([0, 1]).all():
        raise ValueError('Missing/invalid target; requires review.')
    if raw.URL.isna().any() or not raw.URL.map(lambda u: isinstance(u, str)).all():
        raise ValueError('Missing/nontext URL; requires source review.')
    if raw.groupby('URL').label.nunique().gt(1).any():
        raise ValueError('Conflicting targets for an exact URL.')
    if set(manifest.columns) != {'source_row', 'partition'} or manifest.source_row.duplicated().any():
        raise ValueError('Invalid split manifest.')
    if not pd.api.types.is_integer_dtype(manifest.source_row):
        raise ValueError('Manifest row positions must be integers.')
    split = manifest.set_index('source_row').sort_index()
    if not split.index.equals(raw.index) or not split.partition.isin(['train','validation','test']).all():
        raise ValueError('Incomplete/invalid split assignments.')
    if split.partition.nunique() != 3:
        raise ValueError('All three partitions must be present.')
    if split.assign(URL=raw.URL).groupby('URL').partition.nunique().gt(1).any():
        raise ValueError('Exact URL crosses split partitions.')
    records, rejected = [], []
    # Compute once per exact input without constructing hundreds of thousands
    # of pandas group frames. Input rows are ordered source positions.
    representative_rows = raw.index[~raw.URL.duplicated(keep='first')]
    labels = raw.label.to_numpy()
    partitions = split.partition.to_numpy()
    url_values = raw.URL.to_numpy()
    rejected_urls = {}
    for representative in representative_rows:
        url = url_values[representative]
        try:
            values = extract_url_features(url)
            host = hostname_group(url)
        except ValueError as exc:
            rejected_urls[url] = str(exc)
            continue
        # Same URL and checked same target => same lexical X/y, irrespective of old content features.
        records.append({'source_row':representative, 'URL':url, 'hostname_group':host,
                        'original_label':int(labels[representative]),
                        'partition':partitions[representative], **values})
    if rejected_urls:
        rejected = [{'source_row':int(i),'reason':rejected_urls[url]}
                    for i,url in enumerate(url_values) if url in rejected_urls]
    if not records:
        raise ValueError('No valid URL records; requires review.')
    prepared = pd.DataFrame(records).set_index('source_row').sort_index()
    if prepared.groupby('hostname_group').partition.nunique().gt(1).any():
        raise ValueError('Parsed hostname crosses split partitions.')
    X = prepared.loc[:, list(FEATURE_NAMES)].copy()
    if not np.isfinite(X.to_numpy()).all():
        raise ValueError('Nonfinite lexical features.')
    y = (1-prepared.original_label).rename('is_phishing').to_frame()
    metadata = prepared[['URL','hostname_group','original_label','partition']].copy()
    reps = prepared.reset_index().set_index('URL').source_row
    mapping = pd.DataFrame({'source_row':raw.index,'partition':split.partition.to_numpy(),
                           'representative_source_row':raw.URL.map(reps).astype('Int64')})
    mapping['status'] = np.where(mapping.representative_source_row.isna(),'quarantined',
                                np.where(mapping.source_row.eq(mapping.representative_source_row).fillna(False),'representative','duplicate_mapped'))
    quarantine = pd.DataFrame(rejected,columns=['source_row','reason']).sort_values('source_row')
    if not X.index.equals(y.index) or not X.index.equals(metadata.index):
        raise AssertionError('X/y/metadata are misaligned.')
    assert len(raw) == len(X) + int(mapping.status.eq('duplicate_mapped').sum()) + len(quarantine)
    assert not metadata.URL.duplicated().any()
    return {'X':X, 'y':y, 'metadata':metadata, 'mapping':mapping, 'quarantine':quarantine}


def prepare_project(root: Path) -> dict:
    """Verify source/split locks and export versioned, separate local files."""
    root = Path(root).resolve()
    source = root/'data/raw/PhiUSIIL_Phishing_URL_Dataset.csv'
    manifest_path = root/'data/processed/split_manifest.csv'
    lock_path = root/'data/processed/split_metadata.json'
    protected = [source,manifest_path,lock_path,root/'src/backend_api/main.py',root/'notebooks/01_eda.ipynb']
    hashes = {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    lock = json.loads(lock_path.read_text(encoding='utf-8'))
    if lock['source_sha256'] != hashes[str(source)] or lock['group_rule'] != 'parsed_hostname_idna_lower_strip_trailing_dot_v1':
        raise ValueError('Source hash or grouping contract differs from locked EDA.')
    raw = pd.read_csv(source)
    manifest = pd.read_csv(manifest_path)
    tables = prepare_rows(raw,manifest)
    metadata = tables['metadata']
    splits = metadata.groupby('partition',sort=True).agg(rows=('URL','size'),host_groups=('hostname_group','nunique'))
    report = root/'reports/data_preparation'
    output = root/'data/processed'/SCHEMA_VERSION
    report.mkdir(parents=True,exist_ok=True)
    output.mkdir(parents=True,exist_ok=True)
    names={'X':'features.csv','y':'target.csv','metadata':'metadata.csv','mapping':'source_mapping.csv','quarantine':'quarantine.csv'}
    for name,filename in names.items():
        tables[name].to_csv(output/filename,index=name in {'X','y','metadata'},index_label='source_row')
    splits.to_csv(report/'partition_summary.csv')
    summary={'schema':SCHEMA_VERSION,'source_rows':len(raw),'output_rows':len(tables['X']),
             'duplicate_rows_mapped':int(tables['mapping'].status.eq('duplicate_mapped').sum()),
             'quarantined_rows':len(tables['quarantine']),'feature_names':list(FEATURE_NAMES),
             'target':'is_phishing: 1 phishing, 0 legitimate',
             'dedup_policy':'exact URL; first source row; original partition preserved',
             'source_sha256':lock['source_sha256'], 'manifest_sha256':hashes[str(manifest_path)],
             'extractor_sha256':hashlib.sha256((root/'src/features/url_features.py').read_bytes()).hexdigest(),
             'preparation_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'output_sha256':{filename:hashlib.sha256((output/filename).read_bytes()).hexdigest() for filename in names.values()},
             'environment':{'python':platform.python_version(),'pandas':importlib.metadata.version('pandas'),'numpy':importlib.metadata.version('numpy')},
             'learned_preprocessing':False,'api_modified':False,
             'row_key':'source_row is metadata/index, never a predictor',
             'invalid_input_policy':'Quarantine with reason; conflicting labels/splits stop run'}
    (report/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (output/'schema.json').write_text(json.dumps({'schema':SCHEMA_VERSION,'features':list(FEATURE_NAMES),
        'target':'is_phishing','positive_class':'phishing','join_key':'source_row','predictor_selection':'select only features in this ordered list'},indent=2),encoding='utf-8')
    assert hashes=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    return {'tables':tables,'summary':summary,'partition_summary':splits}
