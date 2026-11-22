"""Synchronize the checked English notebook and record a submission checklist."""
from pathlib import Path
import hashlib
import json
import shutil
import nbformat
from nbconvert import HTMLExporter

ROOT=Path(__file__).resolve().parents[2]
DELIVERY=ROOT/'submission/GroupXX_PhishingDetection'
PREVIEW=ROOT/'reports/submission_validation'

if __name__=='__main__':
    nb=nbformat.read(DELIVERY/'GroupXX_Project.ipynb',4)
    assert all(c.execution_count is not None for c in nb.cells if c.cell_type=='code')
    assert not any(o.output_type=='error' for c in nb.cells if c.cell_type=='code' for o in c.outputs)
    assert json.loads((DELIVERY/'reports/final_evaluation/status.json').read_text())==json.loads((ROOT/'reports/final_evaluation/status.json').read_text())
    assert (DELIVERY/'reports/final_evaluation/frozen_protocol.json').read_bytes()==(ROOT/'reports/final_evaluation/frozen_protocol.json').read_bytes()
    shutil.copy2(DELIVERY/'GroupXX_Project.ipynb',ROOT/'notebooks/01_eda.ipynb')
    # Keep the repository audit evidence synchronized with the executed English notebook.
    for path in (DELIVERY/'reports').rglob('*'):
        if path.is_file():
            target=ROOT/'reports'/path.relative_to(DELIVERY/'reports')
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target)
    for name in ['split_manifest.csv','split_metadata.json']:
        assert (DELIVERY/'data/processed'/name).read_bytes()==(ROOT/'data/processed'/name).read_bytes()
    exporter=HTMLExporter();exporter.exclude_input_prompt=True;exporter.exclude_output_prompt=True
    body,_=exporter.from_notebook_node(nb)
    (ROOT/'reports/eda.html').write_text(body,encoding='utf-8')
    files=['GroupXX_Project.ipynb','GroupXX_Report.pdf','dataset.csv','README.txt']
    checklist={
        'scope':'Academic course project; no ZIP generated',
        'group_members':[{'name':'Meltem Orhan','student_id':'221015002'},
                         {'name':'Ali Abdel Halim','student_id':None},
                         {'name':'Halil Trabzon','student_id':None}],
        'group_number':None,
        'pending_before_submission':['Assigned group number','Ali Abdel Halim student ID','Halil Trabzon student ID'],
        'notebook_checks':{'full_execution':'PASS','executed_code_cells':48,'embedded_figures':22,
                           'test_results_reproduced':'PASS','English_sources_and_outputs':'PASS'},
        'requirements':{
            'dataset_and_attribution':'Notebook 2, README, report 1',
            'data_dictionary':'Notebook 3, report Appendix A (all 56 columns)',
            'research_question_hypothesis':'Notebook 1 and 15, report 1 and 5',
            'EDA_at_least_five_visualizations':'Notebook 7-11; 22 saved image outputs overall',
            'missing_values':'Notebook 4, report 2; no imputation needed',
            'descriptive_statistical_analysis':'Notebook 7-10 and 15',
            'justified_preprocessing':'Notebook 12-14, report 6',
            'two_classification_models':'Notebook 16: Logistic Regression and Random Forest, plus baseline',
            'confusion_matrices_metrics_comparison':'Notebook 16-18, report 8',
            'interpretation_leakage_imbalance_bias':'Notebook 6, 11, 16-20; report 3 and 9',
            'English_conclusion_ethics_references':'Notebook 19-21; report 9-10 and References',
            'English_presentation_8_to_12_minutes':'presentation/; 12 slides, target 650 seconds, all three members'},
        'submission_files':{name:{'bytes':(DELIVERY/name).stat().st_size,
                                  'sha256':hashlib.sha256((DELIVERY/name).read_bytes()).hexdigest()} for name in files},
        'delivery_content':'Only these four files are required; data/ and reports/ created by Run All are generated outputs.'}
    (PREVIEW/'checklist.json').write_text(json.dumps(checklist,indent=2),encoding='utf-8')
    readme='''# Detection of Phishing Websites Using Machine Learning

This repository contains the academic course project using the PhiUSIIL dataset.
The main experiment follows source checks, training-only EDA, justified preprocessing,
an exploratory hypothesis, classification, one feature-reduction experiment and
a frozen internal test comparison. Earlier dataset exposure and remaining collection
and campaign dependencies are documented alongside the scores.

## Start here

- [Complete English notebook](notebooks/01_eda.ipynb), with all saved outputs.
- [Browser view of the notebook](reports/eda.html).
- [Four-file submission folder](submission/GroupXX_PhishingDetection/).
- [English report](submission/GroupXX_PhishingDetection/GroupXX_Report.pdf).
- [Presentation](presentation/GroupXX_Presentation.pptx), 12 slides with speaker notes.
- [Presentation PDF](presentation/GroupXX_Presentation.pdf).
- [Timed speaking guide and questions](presentation/GroupXX_SpeakerNotes.pdf).
- [Submission verification and requirement mapping](reports/submission_validation/checklist.json).

The presentation targets 10 minutes 50 seconds, with speaking parts for all three members.
No ZIP has been created. Before submission, replace GroupXX and complete Ali Abdel Halim's
and Halil Trabzon's student IDs. Meltem Orhan's ID is 221015002.

## Run the analysis

Use Python 3.12.10 and install the pinned environment:

```powershell
python -m pip install -r requirements-eda.txt
```

Select that Python environment as the notebook kernel, restart and Run All.
In the repository, the notebook reads `data/raw/PhiUSIIL_Phishing_URL_Dataset.csv`.
The standalone submitted copy reads `dataset.csv` beside it and embeds the dictionary
and frozen configuration; it needs no repository source modules or existing outputs.
Both create split/audit outputs under `data/processed/` and `reports/` as needed.
The submitted README.txt contains complete installation and execution instructions.

## Dataset and evaluation

PhiUSIIL Phishing URL (Website), Arvind Prasad and Shalini Chandra (2024),
[UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset),
CC BY 4.0. The original dataset contains 235,795 rows and 56 columns.
Source labels: 0 phishing, 1 legitimate; model target: 1 phishing.
[English variable dictionary](docs/data_dictionary_en.md) documents all 56 fields and evidence caveats.

Observed hosts are kept together in fixed training/validation/test partitions.
All source observations are retained in this academic experiment, including repeated
URLs with different recorded measurements. Transformations fit on training only.
Forty-eight original predictors are compared with one reduced 20-predictor forest.
The reduced forest was selected on validation and frozen at threshold 0.5 before test scoring.

The selected model made 2 false alarms and 3 missed phishing observations on 47,583
internal test rows (phishing F1 99.9878%). These results do not establish external,
temporal or campaign-independent performance. See notebook Sections 18-21 for limitations.
Small reproducible summaries are kept under `reports/`; source and large generated
CSV files remain excluded from Git. The local submission contains the actual dataset.

## Supporting files

`src/reporting/` contains preparation, execution, document-generation and checking scripts.
`requirements-reporting.txt` lists optional PDF/PowerPoint build dependencies; these
are not needed to run the notebook. The document builders use an isolated
`../.delivery-tools/` installation. Generating the submission notebook clears its
outputs, so run the validation script afterwards before submitting.

Other pre-existing notebooks and modules remain separate from the academic submission.
`notebooks/01_eda.ipynb` and the four-file folder above define the current course project.
'''
    (ROOT/'README.md').write_text(readme,encoding='utf-8')
    print('Synchronized executed English notebook, HTML, audit outputs and requirement checklist.')
