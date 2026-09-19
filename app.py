from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import joblib
import os
from sqlalchemy.orm import Session
from database import SessionLocal, PredictionLog, init_db

app = FastAPI(title="Spam Email Classifier API")

# Khởi tạo bảng dữ liệu khi server khởi chạy
init_db()

# Dependency lấy Session làm việc với DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

MODEL_PATH = os.path.join(os.path.dirname(__file__), "spam_model_kaggle_optimized.pkl")

model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"Error loading model: {e}")

class EmailRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Spam Classifier API is running."}

@app.post("/predict")
def predict_spam(email: EmailRequest, db: Session = Depends(get_db)):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded on the server")
    
    prediction = model.predict([email.text])[0]
    
    # Lưu kết quả vào Cơ sở dữ liệu
    log_entry = PredictionLog(email_content=email.text, prediction=prediction)
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    
    return {
        "id": log_entry.id,
        "email_content": email.text,
        "prediction": prediction,
        "created_at": log_entry.created_at
    }

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    # Lấy lịch sử 10 lần dự đoán gần nhất
    logs = db.query(PredictionLog).order_by(PredictionLog.id.desc()).limit(10).all()
    return logs