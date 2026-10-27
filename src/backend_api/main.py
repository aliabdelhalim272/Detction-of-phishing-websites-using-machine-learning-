from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(
    title="Phishing Detection API",
    description="API to detect if a URL is Phishing or Legitimate using Machine Learning",
    version="1.0.0"
)

class URLScanRequest(BaseModel):
    url: str

MODEL_PATH = "models/phishing_model.pkl"
model = None

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
else:
    print("Model not found. Using dummy logic.")

def extract_url_features(url: str) -> dict:
    return {
        "url_length": len(url),
        "has_at_symbol": 1 if "@" in url else 0,
        "has_dash": 1 if "-" in url else 0,
        "count_dots": url.count("."),
        "has_https": 1 if url.startswith("https") else 0
    }

@app.get("/")
def read_root():
    return {"message": "Welcome to the Phishing Detection API!"}

@app.post("/api/v1/scan")
def scan_url(request: URLScanRequest):
    url = request.url
    
    if not url.strip():
        raise HTTPException(status_code=400, detail="Invalid URL provided.")

    if model is not None:
        features_dict = extract_url_features(url)
        features_df = pd.DataFrame([features_dict])
        
        prediction = model.predict(features_df)[0]
        probabilities = model.predict_proba(features_df)[0]
        confidence = float(max(probabilities))
        
        is_phishing = bool(prediction == 1)
    else:
        suspicious_words = ["login", "update", "verify", "secure", "bank", "account"]
        is_phishing = any(word in url.lower() for word in suspicious_words) or "-" in url
        confidence = 0.98 if is_phishing else 0.85

    return {
        "url": url,
        "prediction": "Phishing" if is_phishing else "Legitimate",
        "is_phishing": is_phishing,
        "confidence_score": round(confidence * 100, 2),
        "message": "Warning: Malicious URL detected!" if is_phishing else "URL is safe."
    }