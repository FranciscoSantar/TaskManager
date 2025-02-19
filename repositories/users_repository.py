from models import Users
from app import db
from werkzeug.security import generate_password_hash

class UsersRepository():
    def __init__(self)->None:
        self.model = Users


    def register(self, username:str, password:str) -> Users:
        hashed_password = generate_password_hash(password)
        new_user = Users(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_user_by_id(self, id:int) -> Users:
        user = db.session.query(self.model).filter_by(id=id).first()
        return user

    def get_user_by_username(self, username:str) -> Users:
        user = db.session.query(self.model).filter_by(username=username).first()
        return user