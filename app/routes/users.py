from flask import Blueprint, jsonify, request
from app.controllers.user_controller import UsersController
from app.services.users_service import UsersService

user_router = Blueprint(name='user_route', import_name=__name__, url_prefix='/')

@user_router.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    response, status_code = UsersController().register(username=username, password=password)

    return response, status_code

@user_router.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    response, status_code = UsersController().login(username=username, password=password)
    return response, status_code
