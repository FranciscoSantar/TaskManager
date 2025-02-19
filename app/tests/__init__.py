from flask import jsonify
import pytest
import datetime
from app import create_app, db
from app.services.users_service import UsersService

@pytest.fixture()
def app():
    app = create_app(testing=True)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()
@pytest.fixture()
def client(app):
    with app.app_context():
        return app.test_client()

@pytest.fixture
def valid_task():
    return {
        "title": "Test Task",
        "status": "To Do",
        "description": "Description of Test Task."
    }

@pytest.fixture
def valid_user():
    return {
        "username":"admin",
        "password":"admin"
    }

@pytest.fixture
def valid_task_serialize():
    return {
        'id': 1,
        'title': 'Test Task',
        'status': 'To Do',
        'description': 'Description of Test Task.',
        'created_at': datetime.datetime(2025, 2, 17, 20, 59, 11),
        'updated_at': datetime.datetime(2025, 2, 17, 20, 59, 11)
    }

@pytest.fixture
def valid_user_serialize():
    return {
        'id': 1,
        'username': 'admin',
        'created_at': datetime.datetime(2025, 2, 17, 20, 59, 11),
        'updated_at': datetime.datetime(2025, 2, 17, 20, 59, 11)
    }

@pytest.fixture
def valid_list_of_task_objects_serialize():
    return [{
        'id': 1,
        'title': 'Test Task',
        'status': 'To Do',
        'description': 'Description of Test Task.',
        'created_at': datetime.datetime(2025, 2, 17, 20, 59, 11),
        'updated_at': datetime.datetime(2025, 2, 17, 20, 59, 11)
    },
    {
        'id': 2,
        'title': 'Test Task 2',
        'status': 'To Do',
        'description': 'Description of Test Task 2.',
        'created_at': datetime.datetime(2025, 2, 17, 20, 59, 11),
        'updated_at': datetime.datetime(2025, 2, 17, 20, 59, 11)
    }]

@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()
        db.session.close()

@pytest.fixture
def valid_token(app):
    with app.app_context():
        token = UsersService().create_token(username='testuser')
        return token

@pytest.fixture
def standard_response(app):
    def _generate_response(message, status="success", data=None, token=None):
        with app.app_context():
            if token:
                response = {
                    "status": status,
                    "message": message,
                    "token": token
                }
            else:
                response = {
                    "status": status,
                    "message": message,
                    "data": data
                }
            return jsonify(response)
    return _generate_response

@pytest.fixture
def error_response_login(app):
    def _generate_response(message, status="success"):
        with app.app_context():
            response = {
                    "status": status,
                    "message": message
                }
            return jsonify(response)
    return _generate_response