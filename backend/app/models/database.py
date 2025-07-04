import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from app.core.config import settings

# Check if running on Vercel
IS_VERCEL = os.environ.get("VERCEL", "0") == "1"

# Use in-memory SQLite for Vercel environment
if IS_VERCEL:
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
else:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define CodeComparison model
class CodeComparison(Base):
    __tablename__ = "code_comparisons"

    id = Column(Integer, primary_key=True, index=True)
    file1_name = Column(String, index=True)
    file1_content = Column(String)
    file1_language = Column(String)
    file2_name = Column(String, index=True)
    file2_content = Column(String)
    file2_language = Column(String)
    similarity_score = Column(Float)
    analysis_result = Column(String)
    is_plagiarized = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()