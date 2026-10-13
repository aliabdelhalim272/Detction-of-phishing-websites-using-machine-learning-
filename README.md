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
