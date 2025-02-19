from flask import jsonify
from models import Users
from app.repositories.users_repository import UsersRepository
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

class UsersService():
    def __init__(self)->None:
        self.model = Users

    def register(self, username:str, password:str):
        """ Validate user information for register process.

        Args:
            username (str):
            password (str):

        Returns:
            tuple: (Success_user_registration, message, UsersObject)
        """
        check_user_information, message = self.check_information(username=username, password=password)
        if not check_user_information:
            user = None
            return check_user_information, message, user
        check_existing_info, message = self.check_existing_user(username=username)
        if not check_existing_info:
            user = None
            return check_existing_info, message, user
        success = True
        user = UsersRepository().register(username=username, password=password)
        message = 'User created successfully.'
        return success, message, user

    def login(self, username:str, password:str):
        """ Validate user information for login process.

        Args:
            username (str):
            password (str):

        Returns:
            tuple: (Success_user_login, message, token)
        """
        check_user_information, message = UsersService().check_information(username=username, password=password)
        if not check_user_information:
            token = None
            return check_user_information, message, token
        check_existing_info, message = UsersService().check_not_existing_user(username=username)
        if not check_existing_info:
            token = None
            return check_existing_info, message, token

        check_user_credentials, message = UsersService().check_credentials(username=username, password=password)
        if not check_user_credentials:
            token = None
            return check_user_credentials, message, token
        success = True
        token = UsersService().create_token(username=username)
        message = 'Login successfully.'
        return success, message, token

    def check_information(self, username:str, password:str):
        '''
        Check if username and password exists
        '''
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

    def check_existing_user(self, username:str):
        '''
        Check if already exists an user with an specific username.
        '''
        existing_user = UsersRepository().get_user_by_username(username=username)
        if existing_user:
            success = False
            message = 'Already exists an user with that username.'
            return success, message
        success = True
        message = ""
        return success, message

    def check_not_existing_user(self, username:str):
        '''
        Check if doesn't exists an user with an specific username.
        '''
        existing_user = UsersRepository().get_user_by_username(username=username)
        if not existing_user:
            success = False
            message = 'There is no user registered with that username.'
            return success, message
        success = True
        message = ""
        return success, message

    def check_credentials(self, username:str, password:str):
        '''
        Check if username and password are valid
        '''
        user = UsersRepository().get_user_by_username(username=username)
        valid_credentials = check_password_hash(user.password, password=password)
        if not valid_credentials:
            success = False
            message = 'Incorrect Password. Try again.'
            return success, message
        success = True
        message = ""
        return success, message

    def create_token(self, username:str):
        '''
        Create a JWT token when a user is loged in
        '''
        access_token = create_access_token(identity=username)
        return access_token

    def get_response_user_register(self, success:bool, message:str, user:Users):
        '''
        Obtain response and status code for HTTP request when an user wants to register
        '''
        if not success:
            return jsonify({
                'status': 'error',
                'message': message,
                'data':None}), 400

        return jsonify({
            'status': 'success',
            'message': message,
            'data':user.serialize()}), 201

    def get_response_user_login(self, success:bool, message:str, token:str):
        '''
        Obtain response and status code for HTTP request when an user wants to login
        '''
        if not success:
            return jsonify({
                'status': 'error',
                'message': message}), 400

        return jsonify({
            'status': 'success',
            'message': message,
            'token':token}), 200

    def get_unexpected_error_response(self):
        '''
        Obtain response and status code for unexpected error
        '''
        return jsonify({
                "status": "error",
                "message": "An unexpected error occurred. Please try again later."
                }), 500