import pytest
from app import create_app
import datetime
from models import Tasks

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
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
    },
    ]