from sqlalchemy import Integer, String, DateTime
from app import db
from datetime import datetime

class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(Integer, primary_key= True)
    title = db.Column(String, nullable = False)
    description = db.Column(String, nullable = True)
    status = db.Column(String, nullable=False)
    created_at = db.Column(DateTime, default=datetime.now())
    updated_at = db.Column(DateTime, default=datetime.now(), onupdate=datetime.now())

