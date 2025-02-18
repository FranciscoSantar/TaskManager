from . import valid_task, app, client, valid_task_serialize
from unittest.mock import patch
from controllers.task_controller import TaskController
from datetime import datetime
from data.tasks_phases import TaskPhases

URL_PREFIX = '/task'

### CREATE TASK TESTS

def test_create_valid_task(client, valid_task):
    with patch.object(TaskController, 'create_task', return_value=(True, "Task created successfully.")) as mock_create_task:
        response = client.post(f"{URL_PREFIX}/", json=valid_task)
        assert response.status_code == 201
        assert response.json == {'message': 'Task created successfully.'}

def test_create_task_without_title(client):
    body = {
        "description": "Description of Test Task.",
        "status": "In Progress"
    }
    response = client.post(f"{URL_PREFIX}/", json=body)
    assert response.status_code == 400
    assert response.json == {'error': 'A task must have a title.'}

def test_create_task_with_invalid_status(client, valid_task):
    valid_task['status'] = 'QWERTY'
    response = client.post(f"{URL_PREFIX}/", json=valid_task)
    assert response.status_code == 400
    posibles_task_states = TaskPhases.get_all_phases()
    message = 'The status of a task only can be:'
    for task_status in posibles_task_states:
        message += f' {task_status},'
    message = message[:-1] + "."
    assert response.json == {'error': message}


### GET TASK BY ID TESTS


def test_get_task_by_valid_id(client, valid_task_serialize):
    with patch.object(TaskController, 'get_task_by_id', return_value=(True, None, valid_task_serialize)) as mock_get_task:
        response = client.get(f"{URL_PREFIX}/1")
        response_data = response.json['task']
        for key in ['created_at', 'updated_at']:
            response_data[key] = datetime.strptime(response_data[key], '%a, %d %b %Y %H:%M:%S GMT')
        assert response.status_code == 200
        assert response_data == valid_task_serialize

def test_get_task_by_alphabetic_id(client):
    response = client.get(f"{URL_PREFIX}/qwerty1")
    assert response.status_code == 400
    assert response.json == {'error': 'Task ID has to be a number.'}

def test_get_task_by_zero_id(client):
    response = client.get(f"{URL_PREFIX}/0")
    assert response.status_code == 400
    assert response.json == {'error': 'Task ID has to be a positive number.'}