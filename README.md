# Detction-of-phishing-websites-using-machine-learning-
An end-to-end Machine Learning system designed to detect phishing websites by analyzing URL features, powered by a real-time Backend API for instant URL scanning.
# 🛡️ Detection of Phishing Websites using Machine Learning

## 📖 About The Project
This is a graduation project focused on cybersecurity and artificial intelligence. The system is designed to detect phishing URLs using Machine Learning algorithms. By extracting specific numerical and structural features from a given URL, our ML model classifies the link as either **Phishing (Malicious)** or **Legitimate (Safe)**.

## 👥 Team Members & Roles
1. **Meltem Orhan** - Data & Feature Engineer
2. **Halil Trabzon** - AI & ML Model Engineer
3. **Aly Abdelhalim** - Backend & Integration Engineer

## 🏗️ System Architecture
The project is divided into three main pipelines:
* **Data Pipeline:** Data collection, cleaning, and feature extraction (URL-based, Domain-based, and Page-based features).
* **ML Pipeline:** Training and hyperparameter tuning of classification models (e.g., Random Forest, SVM).
* **Backend & Integration:** A RESTful API built to serve the trained ML model and handle incoming URL scan requests.

## 📁 Repository Structure
* `data/`: Contains raw and processed data (Note: Large datasets are ignored by git).
* `notebooks/`: Jupyter notebooks for data exploration and model training.
* `src/`: Source code for feature extraction and the backend API.
* `models/`: Exported trained ML models.
* `docs/`: Project documentation and API specs.


## Completed offline analysis

```text
notebooks/01_analysis_and_modeling.ipynb  # Executed analysis and model comparison
data/raw/                              # Original CSV, ignored by Git
data/processed/                        # Reserved for derived data, ignored by Git
reports/analysis.html                  # Browser-readable notebook export
reports/results/                       # Metrics, audits, split manifest and figures
reports/presentation/                  # Presentation HTML and speaker notes
scripts/prepare_project.py             # Rebuild notebook source (clears outputs)
scripts/prepare_delivery.py            # Refresh HTML and presentation from saved results
requirements-analysis.txt              # Verified analysis dependencies
```

Use Python 3.12 in a separate analysis environment. From the repository root:

```powershell
python -m venv .venv-analysis
.\.venv-analysis\Scripts\python.exe -m pip install -r requirements-analysis.txt
.\.venv-analysis\Scripts\python.exe -m ipykernel install --user --name phishing-analysis --display-name "Python 3.12 (Phishing Analysis)"
```

Select that kernel and run `notebooks/01_analysis_and_modeling.ipynb` from the
repository root or its notebooks directory. The committed notebook retains the
previously executed results; only its file paths were updated during organization.
Place `PhiUSIIL_Phishing_URL_Dataset.csv` in `data/raw/` before running it.
No URLs are fetched during analysis. Run All regenerates `reports/results/`.

After a successful notebook run, refresh the browser report and presentation:

```powershell
.\.venv-analysis\Scripts\python.exe scripts/prepare_delivery.py
```

`prepare_project.py` intentionally rebuilds the notebook without execution outputs;
run it only when rebuilding, then execute the notebook before exporting.
The exporter preserves this README and both dependency files.
The root `requirements.txt` remains the existing backend dependency file.

Dataset: [PhiUSIIL, UCI](https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset),
Arvind Prasad and Shalini Chandra (2024), CC BY 4.0.
Original label: 0 phishing, 1 legitimate. Analysis positive class: phishing (1).
Data fingerprint and environment are in `reports/results/run_metadata.json`.

The offline models use 47 numeric features, including webpage-content features.
The API currently extracts five URL features and falls back to heuristic rules
when no model is available. The analyzed models are not integrated into the API.
Observed-domain-separated internal scores do not establish temporal, campaign,
registered-domain or external generalization. Feature definitions include inferred
meanings; see the notebook for limitations and references.
