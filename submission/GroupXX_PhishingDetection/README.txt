DETECTION OF PHISHING WEBSITES USING MACHINE LEARNING
GroupXX - academic project submission

BEFORE SUBMISSION
Replace GroupXX with the assigned group number in folder and file names.
Add Ali Abdel Halim's and Halil Trabzon's student IDs in this README,
the notebook title page and the report/presentation title pages.
Current files deliberately retain these unknown fields as TO BE ADDED.

GROUP MEMBERS
Meltem Orhan - 221015002
Ali Abdel Halim - TO BE ADDED
Halil Trabzon - TO BE ADDED

PROJECT DESCRIPTION
We study whether recorded URL and webpage features distinguish phishing from
legitimate websites in the PhiUSIIL dataset. The notebook documents integrity
checks, training-only EDA, a testable exploratory hypothesis, justified encoding
and scaling, a majority baseline, Logistic Regression, Random Forest, controlled
feature reduction, and a frozen internal test comparison. Source rows/values
are retained. Results do not establish performance on other datasets.

DATASET AND ATTRIBUTION
PhiUSIIL Phishing URL (Website), Arvind Prasad and Shalini Chandra, 2024.
UCI Machine Learning Repository, dataset 967. License: CC BY 4.0.
Dataset record: https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset
Direct source download: https://archive.ics.uci.edu/static/public/967/phiusiil+phishing+url+dataset.zip
Associated paper: https://doi.org/10.1016/j.cose.2023.103545
dataset.csv is the original PhiUSIIL_Phishing_URL_Dataset.csv, renamed only.
235,795 rows; 56 columns. It has not been cleaned or overwritten in place.
SHA-256: a236549cd369cd80bd478ff8e1779cbf44c58d5c3f79f7a51a1adbed7d06d1c6
Original label: 0 = phishing, 1 = legitimate.
Model target: y = 1 - label, so positive class 1 = phishing.
See notebook Section 3 for the full data dictionary and definition caveats.

SUBMITTED FILES
GroupXX_Project.ipynb - complete English notebook with saved tables/figures.
GroupXX_Report.pdf - English methods, findings, interpretation and references.
dataset.csv - original source data, required beside the notebook.
README.txt - attribution, group information and execution instructions.
The 8-12 minute English presentation and speaker notes are supplied separately
in the repository's presentation/ folder. No ZIP has been created.

HOW TO RUN
1. Extract/copy the entire submission folder to a writable local directory.
2. Use Python 3.12.10 (the tested interpreter) in a dedicated environment.
3. Install the exact libraries below. From this folder in PowerShell:
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install numpy==2.4.4 pandas==3.0.2 matplotlib==3.10.9 scikit-learn==1.8.0 scipy==1.17.1 nbformat==5.10.4 nbclient==0.11.0 nbconvert==7.17.1 ipykernel==7.2.0
4. Open GroupXX_Project.ipynb in VS Code with Python and Jupyter extensions
   (or an existing Jupyter frontend), and select this environment as the kernel.
5. Restart the kernel and Run All from the first cell to the last.
   Keep dataset.csv beside the notebook. No src/, docs/, downloaded model,
   API, network access or previously generated experiment files are required.
6. The notebook creates data/processed/ and reports/ under its working folder.
   These include split manifests, audit tables and image files. They are outputs,
   not additional inputs. Running may take several minutes and use significant
   memory; elapsed times depend on the computer. Random Forest uses two workers.
7. Save the executed notebook so every table and figure remains visible.

PINNED PYTHON LIBRARIES
numpy==2.4.4
pandas==3.0.2
matplotlib==3.10.9
scikit-learn==1.8.0
nbformat==5.10.4
nbclient==0.11.0
nbconvert==7.17.1
ipykernel==7.2.0
scipy==1.17.1

REPRODUCIBILITY AND INTERPRETATION
Seed 42; observed URL-host grouping; approximately 60/20/20 rows in training,
validation and test. Fitted transformations use training only. The selected
20-feature Random Forest and threshold 0.5 were frozen before test scoring.
Re-running repeats that fixed experiment; it must not be used to tune from test
results. Earlier work exposed this dataset, so this is internal evaluation,
not retrospectively unseen external confirmation. Parent-domain, campaign,
template and collection dependencies may remain.

Final internal test: 47,583 observations, accuracy 99.9895%, phishing precision
99.9903%, recall 99.9854%, F1 99.9878%, 2 false alarms and 3 missed phishing rows.
These values describe this experiment only. See Sections 18-21 for limitations,
ethics, conclusion and references.
