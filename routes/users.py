from flask import Blueprint, jsonify, request
from controllers.user_controller import UsersController
from services.users_service import UsersService

user_router = Blueprint(name='user_route', import_name=__name__, url_prefix='/')

@user_router.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    success_register_user, message, new_user = UsersController().register(username=username, password=password)
    response, status_code = UsersService().get_response_user_register(success=success_register_user, message=message)

    return response, status_code

@user_router.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    success_register_user, message, token = UsersController().login(username=username, password=password)
    response, status_code = UsersService().get_response_user_login(success=success_register_user, message=message, token=token)
    return response, status_code
