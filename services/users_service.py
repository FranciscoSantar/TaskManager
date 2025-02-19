from flask import jsonify
from models import Users
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

class UsersService():
    def __init__(self)->None:
        self.model = Users


    def check_information(self, username:str, password:str) -> Users:
        if not username:
            success = False
            message = 'Username input is required.'
            return success, message
        if not password:
            success = False
            message = 'Password input is required.'
            return success, message
        success = True
        message = ""
        return success, message

    def check_existing_user(self, username:str) -> Users:
        existing_user = UsersDatabaseService().get_user_by_username(username=username)
        if existing_user:
            success = False
            message = 'Already exists an user with that username.'
            return success, message
        sucess = True
        message = ""
        return success, message

    def check_not_existing_user(self, username:str) -> Users:
        existing_user = UsersDatabaseService().get_user_by_username(username=username)
        if not existing_user:
            success = False
            message = 'There is no user registered with that username.'
            return success, message
        success = True
        message = ""
        return success, message

    def check_credentials(self, username:str, password:str):
        user = UsersDatabaseService().get_user_by_username(username=username)
        valid_credentials = check_password_hash(user.password, password=password)
        if not valid_credentials:
            success = False
            message = 'Incorrect Password. Try again.'
            return success, message
        success = True
        message = ""
        return success, message

    def create_token(self, username:str):
        access_token = create_access_token(identity=username)
        return access_token

    def get_response_user_register(self, success:bool, message:str):
        if not success:
            return jsonify({
                'status': 'error',
                'message': message}), 400

        return jsonify({
            'status': 'success',
            'message': message}), 201

    def get_response_user_login(self, success:bool, message:str, token:str):
        if not success:
            return jsonify({
                'status': 'error',
                'message': message}), 400

        return jsonify({
            'status': 'success',
            'message': message,
            'token':token}), 200



class UsersDatabaseService():
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