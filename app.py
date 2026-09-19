from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Spam Email Classifier")

class EmailRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Spam Classifier API is running"}

@app.post("/predict")
def predict_spam(email: EmailRequest):
    # TODO: Tích hợp model scikit-learn vào đây
    # Tạm thời trả về kết quả giả lập (mock data)
    return {
        "email_content": email.text,
        "prediction": "spam",
        "confidence": 0.99
    }
