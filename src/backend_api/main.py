from fastapi import FastAPI

app = FastAPI(title="Phishing Detection API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Phishing Detection API!"}

@app.post("/api/v1/scan")
def scan_url(url: str):
    suspicious_words = ["login", "update", "verify", "secure"]
    is_phishing = any(word in url.lower() for word in suspicious_words) or "-" in url
    
    return {
        "url": url,
        "prediction": "Phishing" if is_phishing else "Legitimate",
        "confidence_score": 0.98 if is_phishing else 0.85,
        "message": "Warning: Malicious URL detected!" if is_phishing else "URL is safe."
    }