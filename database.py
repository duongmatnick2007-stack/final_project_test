import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Lấy URL kết nối từ biến môi trường (mặc định dùng SQLite ở local)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# Xử lý tương thích chuỗi kết nối của Render/Koyeb (nếu bắt đầu bằng postgres://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Schema lưu lịch sử dự đoán (Đạt chuẩn 3NF)
class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    email_content = Column(String, nullable=False)
    prediction = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)