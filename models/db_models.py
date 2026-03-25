"""
SQLAlchemy database models
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_premium = Column(Boolean, default=False)

class OriginalSong(Base):
    __tablename__ = "original_songs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    duration = Column(Float)  # In seconds
    key = Column(String)
    tempo = Column(Float)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

class GeneratedCover(Base):
    __tablename__ = "generated_covers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    original_song_id = Column(String, nullable=False)
    output_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    
    # Configuration
    target_style = Column(String)
    target_raga = Column(String)
    target_instruments = Column(any)  # List as JSON
    processing_mode = Column(String)
    tempo_adjustment = Column(Float)
    energy_level = Column(Float)
    
    # Metadata
    duration = Column(Float)
    quality = Column(String)  # 'high', 'medium', 'low'
    
    # Status
    status = Column(String, default='processing')  # 'processing', 'completed', 'failed'
    error_message = Column(any)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    # User feedback
    rating = Column(Integer)  # 1-5 stars
    feedback = Column(any)

class ProcessingJob(Base):
    __tablename__ = "processing_jobs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    
    # Task info
    celery_task_id = Column(String)
    status = Column(String)  # 'queued', 'processing', 'completed', 'failed'
    progress = Column(Integer, default=0)  # 0-100
    
    # Timing
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    estimated_time_seconds = Column(Integer)
    
    # Result
    result_path = Column(String)
    error_message = Column(any)