# Detection of Phishing Websites Using Machine Learning

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
