from app.tests.utils import format_date_in_response
from app.tests import valid_task, app, client, valid_token, standard_response, valid_user_serialize, valid_user, error_response_login
from unittest.mock import patch
from app.controllers.user_controller import UsersController


URL_PREFIX = ''



### CREATE TASK TESTS



def test_register_valid_user(client, valid_user, valid_user_serialize, valid_token, standard_response):
    message= 'User created successfully.'
    status_code = 201
    mock_response = standard_response(status="success", message=message, data=valid_user_serialize)
    with patch.object(UsersController, 'register', return_value=(mock_response, status_code)):
        response = client.post(f"{URL_PREFIX}/register", json=valid_user)
        response_data = format_date_in_response(response=response)
        assert response.status_code == 201
        assert response_data == {
                                    'status': 'success',
                                    'message': message,
                                    'data': valid_user_serialize
                                }

def test_register_no_username(client, valid_user, valid_token):
    message= 'Username input is required.'
    valid_user['username'] = ''
    response = client.post(f"{URL_PREFIX}/register", json=valid_user)
    assert response.status_code == 400
    assert response.json == {
                                'status': 'error',
                                'message': message,
                                'data': None
                            }

def test_register_no_password(client, valid_user, valid_token):
    message= 'Password input is required.'
    valid_user['password'] = ''
    response = client.post(f"{URL_PREFIX}/register", json=valid_user)
    assert response.status_code == 400
    assert response.json == {
                                'status': 'error',
                                'message': 'Password input is required.',
                                'data': None
                            }

def test_login_valid_user(client, valid_user, valid_token, standard_response):
    message= 'Login successfully.'
    status_code = 200
    mock_response = standard_response(status="success", message=message, token=valid_token)
    with patch.object(UsersController, 'login', return_value=(mock_response, status_code)):
        response = client.post(f"{URL_PREFIX}/login", json=valid_user)
        assert response.status_code == 200
        assert response.json == {
                                    'status': 'success',
                                    'message': message,
                                    'token': valid_token
                                }

def test_login_no_username(client, valid_user):
    message= 'Username input is required.'
    valid_user['username'] = ''
    response = client.post(f"{URL_PREFIX}/login", json=valid_user)
    assert response.status_code == 400
    assert response.json == {
                                'status': 'error',
                                'message': message
                            }

def test_login_no_password(client, valid_user):
    message= 'Password input is required.'
    valid_user['password'] = ''
    response = client.post(f"{URL_PREFIX}/login", json=valid_user)
    assert response.status_code == 400
    assert response.json == {
                                'status': 'error',
                                'message': message
                            }

def test_login_no_existing_user(client, valid_user, error_response_login):
    message= 'There is no user registered with that username.'
    status_code = 400
    mock_response = error_response_login(status="error", message=message)
    with patch.object(UsersController, 'login', return_value=(mock_response, status_code)):
        response = client.post(f"{URL_PREFIX}/login", json=valid_user)
        assert response.status_code == 400
        assert response.json == {
                                    'status': 'error',
                                    'message': message
                                }