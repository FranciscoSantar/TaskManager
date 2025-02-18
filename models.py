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

    def serialize(self):
        columns = self.__table__.columns.keys()
        return {column:getattr(self, column) for column in columns}

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key= True)
    username = db.Column(String, nullable = False)
    password = db.Column(String, nullable = False)
    created_at = db.Column(DateTime, default=datetime.now())
    updated_at = db.Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    def serialize(self):
        columns = self.__table__.columns.keys()
        return {column:getattr(self, column) for column in columns if column != 'password'}

