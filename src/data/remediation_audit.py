"""Trace EDA findings to implemented changes, exclusions and open questions.

Only training rows are inspected in before/after comparisons. Existing prepared
files are verified, not rewritten. Large row-level numeric review stays local.
"""
from pathlib import Path
import hashlib
import json
from urllib.parse import urlsplit
import numpy as np
import pandas as pd
from src.features import FEATURE_NAMES, hostname_group


def audit_preparation(root):
    root=Path(root).resolve()
    output=root/'data/processed/url_lexical_v1'
    report=root/'reports/data_preparation'
    source=root/'data/raw/PhiUSIIL_Phishing_URL_Dataset.csv'
    prepared_summary=json.loads((report/'summary.json').read_text(encoding='utf-8'))
    protected=[source,root/'notebooks/01_eda.ipynb',root/'src/backend_api/main.py',
               root/'data/processed/split_manifest.csv',root/'data/processed/split_metadata.json']
    before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    if before[str(source)]!=prepared_summary['source_sha256']:
        raise ValueError('Source does not match the prepared dataset.')
    for filename,expected in prepared_summary['output_sha256'].items():
        if hashlib.sha256((output/filename).read_bytes()).hexdigest()!=expected:
            raise ValueError('Prepared file changed: '+filename)
    X=pd.read_csv(output/'features.csv',index_col='source_row')
    y=pd.read_csv(output/'target.csv',index_col='source_row')
    metadata=pd.read_csv(output/'metadata.csv',index_col='source_row')
    mapping=pd.read_csv(output/'source_mapping.csv')
    manifest=pd.read_csv(root/'data/processed/split_manifest.csv').set_index('source_row')
    raw=pd.read_csv(source)
    # All partitions: structural guarantees only, no distribution comparisons.
    if tuple(X.columns)!=FEATURE_NAMES or not X.index.equals(y.index) or not X.index.equals(metadata.index):
        raise ValueError('Feature schema or row alignment changed.')
    assert np.isfinite(X.to_numpy()).all()
    assert metadata.URL.is_unique
    assert metadata.groupby('hostname_group').partition.nunique().max()==1
    assert metadata.partition.equals(manifest.loc[metadata.index,'partition'])
    assert y.is_phishing.eq(1-metadata.original_label).all()
    assert len(mapping)==len(raw)
    assert set(mapping.loc[mapping.status.ne('quarantined'),'representative_source_row'].astype(int))==set(X.index)
    # Use the original training partition, including repeated observations, so
    # counts are comparable with EDA. Join each to its retained representative.
    ids=manifest.index[manifest.partition.eq('train')]
    train_raw=raw.loc[ids].copy()
    lineage=mapping.set_index('source_row').loc[ids]
    usable=lineage.status.ne('quarantined')
    train_raw=train_raw.loc[usable]
    rep_ids=lineage.loc[usable,'representative_source_row'].astype(int)
    train_X=X.loc[rep_ids].copy();train_X.index=train_raw.index
    train_meta=metadata.loc[rep_ids].copy();train_meta.index=train_raw.index
    parsed=train_raw.URL.map(urlsplit)
    rules=[
        ('URLLength','url_length',train_raw.URL.str.len()),
        ('IsHTTPS','has_https',parsed.map(lambda p:int(p.scheme.lower()=='https'))),
        ('NoOfEqualsInURL',None,train_raw.URL.str.count('=')),
        ('NoOfQMarkInURL',None,train_raw.URL.str.count(r'\?')),
        ('NoOfAmpersandInURL',None,train_raw.URL.str.count('&')),
        ('NoOfDegitsInURL','digit_count',train_raw.URL.map(lambda s:sum(c in '0123456789' for c in s))),
        ('DegitRatioInURL','digit_ratio',train_X.digit_count/train_X.url_length),
    ]
    comparisons=[];details=[]
    for old,new,expected in rules:
        expected=pd.Series(expected,index=train_raw.index)
        old_ok=np.isclose(train_raw[old].to_numpy(dtype=float),expected.to_numpy(dtype=float),rtol=0,atol=1e-12)
        if new:
            actual=train_X[new]
            new_ok=np.isclose(actual.to_numpy(dtype=float),expected.to_numpy(dtype=float),rtol=0,atol=1e-12)
            assert new_ok.all(), 'Prepared field violates its definition: '+new
            status='new_contract_verified; original_formula_not_claimed'
        else:
            actual=expected
            new_ok=np.ones(len(expected),dtype=bool)
            status='diagnostic_recomputed_only; not_a_model_feature'
        comparisons.append({'recorded_field':old,'prepared_field':new or '[audit only]',
            'training_source_rows':len(train_raw),'old_definition_mismatches':int((~old_ok).sum()),
            'new_definition_mismatches':int((~new_ok).sum()),'status':status})
        changed_ids=train_raw.index[~old_ok]
        details.append(pd.DataFrame({'source_row':changed_ids,'recorded_field':old,
            'recorded_value':train_raw.loc[changed_ids,old].to_numpy(dtype=float),
            'recomputed_value':actual.loc[changed_ids].to_numpy(dtype=float),
            'scope':'prepared_feature' if new else 'diagnostic_only'}))
    comparison=pd.DataFrame(comparisons)
    comparison.to_csv(report/'before_after_training.csv',index=False)
    # These diagnostic fields do not silently extend the 14-feature contract.
    pd.concat(details,ignore_index=True).to_csv(output/'training_correction_details.csv',index=False)
    derived=pd.DataFrame(index=train_raw.index)
    derived['equals_count']=rules[2][2]
    derived['question_mark_count']=rules[3][2]
    derived['ampersand_count']=rules[4][2]
    derived.to_csv(output/'training_diagnostic_counts.csv',index_label='source_row')
    normalized_domain=train_raw.Domain.astype(str).str.strip().str.lower().str.rstrip('.')
    expected_host=train_raw.URL.map(hostname_group)
    assert train_meta.hostname_group.eq(expected_host).all()
    mismatch=normalized_domain.ne(expected_host)
    netloc=parsed.map(lambda p:p.netloc.lower().rstrip('.'))
    has_port=parsed.map(lambda p:p.port is not None)
    has_userinfo=parsed.map(lambda p:p.username is not None)
    domain_cases=pd.DataFrame({'source_row':train_raw.index,'domain_host_different':mismatch,
        'domain_equals_netloc':normalized_domain.eq(netloc),'has_port':has_port,'has_userinfo':has_userinfo})
    domain_cases.loc[mismatch].to_csv(report/'domain_difference_classification.csv',index=False)
    domain_summary={'mismatching_training_rows':int(mismatch.sum()),
        'port_cases':int((mismatch&has_port).sum()),'userinfo_cases':int((mismatch&has_userinfo).sum()),
        'recorded_domain_equals_netloc_rows':int(normalized_domain.eq(netloc).sum()),
        'new_hostname_group_mismatches':int(train_meta.hostname_group.ne(expected_host).sum())}
    ledger_rows=[
        ('source','Raw data unchanged','applied_verified','Source, split, EDA and backend hashes preserved','Original stays authoritative; no overwrite'),
        ('quality','Missing/nonfinite values','no_action_needed','No original missing/infinite cells; new X finite','Future invalid input is rejected/quarantined, not imputed globally'),
        ('target','Opposite source/API target convention','applied_verified','New is_phishing=1; original_label kept outside X','Backend integration is a separate open item'),
        ('duplicates','425 extra URL observations','applied_verified','235370 URL-only representatives; all source lineage retained','Old content observations were not adjudicated'),
        ('split','Group overlap','applied_verified','Original partitions inherited; no observed-host overlap','Registered-domain/campaign independence remains open'),
        ('url_length','Recorded URLLength mismatch','applied_verified_new_contract','New url_length matches original text length','Why the original differs by -1 remains unknown'),
        ('https','HTTPS indicator semantics','applied_verified_new_contract','New has_https uses parsed scheme','Original producer code not verified; no TLS certificate check'),
        ('domain','Netloc versus hostname','applied_verified_new_contract','Separate parsed hostname_group; port/userinfo classified','Original Domain retained; no registered-domain extraction'),
        ('digits','Digit count and ratio','applied_verified_new_contract','ASCII digit_count and documented denominator verified','Original ratio formula not reconstructed'),
        ('special_counts','Equals/question/ampersand mismatches','diagnostic_only_not_selected','Recomputed training counts and differences saved locally','These three counts are not in the 14-field model contract'),
        ('other_ratios','Letters/special/obfuscation formulas','excluded_not_resolved','Not used in first URL-only contract','Original formulas, denominators and rounding remain unverified'),
        ('reference','Three reference scores','excluded_not_resolved','Not in new X; source preserved','Reference population, timing and label use unknown'),
        ('content','Page/title/behavior features','excluded_not_resolved','Not in new X; source preserved','Original HTML/formulas and live retrieval contract needed'),
        ('outliers','Long tails/IQR flags','no_automatic_edit','No mass deletion or clipping','Extreme does not establish error; model transforms belong to Role 2'),
        ('sparsity','Zero-heavy fields','no_automatic_edit','No field dropped solely because it is sparse','Do not equate rare with invalid'),
        ('correlation','Seven strong feature pairs','no_automatic_edit','No correlation-threshold deletion','Final new schema chosen by defined availability, not this threshold'),
        ('tld','TLD/subdomain parsing','excluded_not_resolved','No category encoding or guessed subdomain count','Documented public-suffix policy needed'),
        ('fitting','Imputation/scaling/encoding','not_needed_at_this_stage','No learned transformation applied','Role 2 fits only training data if needed'),
        ('api','Shared extractor integration','open','New module exists; old API unchanged','Wire versioned schema/target with model team'),
        ('external','Prior exposure/external validation','open','Limits documented, no independent-test claim','New external/temporal data required'),
        ('groups','Campaign/registered-domain dependence','open','Observed-host split only','Additional grouping audit required'),
        ('enrichment','Certificate validity/domain age','not_implemented','Not faked as zeros or safety flags','Separate network/data-source work'),
    ]
    ledger=pd.DataFrame(ledger_rows,columns=['id','eda_finding','status','action_or_evidence','remaining_limit'])
    ledger.to_csv(report/'finding_status.csv',index=False)
    audit_summary={'training_source_rows_reviewed':len(train_raw),'retained_training_rows':int(metadata.partition.eq('train').sum()),
        'domain':domain_summary,'status_counts':{str(k):int(v) for k,v in ledger.status.value_counts().items()},
        'scope':'New lexical contract verified; original 56-column dataset is not universally repaired',
        'diagnostic_count_fields_are_model_features':False}
    (report/'remediation_summary.json').write_text(json.dumps(audit_summary,indent=2),encoding='utf-8')
    assert before=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
    return {'comparisons':comparison,'domain':domain_summary,'ledger':ledger,'summary':audit_summary}
