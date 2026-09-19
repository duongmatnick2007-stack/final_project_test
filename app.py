from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI(title="Spam Email Classifier API")

# Sửa lại đúng tên file .pkl thực tế của bạn ở đây:
try:
    model = joblib.load("spam_model_kaggle_optimized.pkl")
    print("Loaded model successfully!")
except FileNotFoundError:
    model = None
    print("Warning: Model file not found. Please check the file name.")

class EmailRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Spam Classifier API is running."}

@app.post("/predict")
def predict_spam(email: EmailRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded on the server")
    
    prediction = model.predict([email.text])[0]
    
    return {
        "email_content": email.text,
        "prediction": prediction
    }