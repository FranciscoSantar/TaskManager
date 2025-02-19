from flask import jsonify
import pytest
from app import create_app, db
import datetime
from models import Tasks
from services.users_service import UsersService

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
def valid_task_object():
    return Tasks(
        id= 1,
        title= 'Test Task',
        status= 'To Do',
        description= 'Description of Test Task.',
        created_at= datetime.datetime(2025, 2, 17, 20, 59, 11),
        updated_at= datetime.datetime(2025, 2, 17, 20, 59, 11)
    )

@pytest.fixture
def valid_list_of_task_objects():
    task_1 = Tasks(
        id= 1,
        title= 'Test Task',
        status= 'To Do',
        description= 'Description of Test Task.',
        created_at= datetime.datetime(2025, 2, 17, 20, 59, 11),
        updated_at= datetime.datetime(2025, 2, 17, 20, 59, 11)
    )
    task_2 = Tasks(
        id= 2,
        title= 'Test Task 2',
        status= 'To Do',
        description= 'Description of Test Task 2.',
        created_at= datetime.datetime(2025, 2, 17, 20, 59, 11),
        updated_at= datetime.datetime(2025, 2, 17, 20, 59, 11)
    )
    return [task_1, task_2]

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
    def _generate_response(message, status="success", data=None):
        with app.app_context():
            response = {
                "status": status,
                "message": message,
                "data": data
            }
            return jsonify(response)
    return _generate_response