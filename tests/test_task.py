from . import valid_task, app, client
from unittest.mock import patch
from controllers.task_controller import TaskController
from data.tasks_phases import TaskPhases

URL_PREFIX = '/task/'

def test_create_valid_task(client, valid_task):
    with patch.object(TaskController, 'create_task', return_value=(True, "Task created successfully.")) as mock_create_task:
        response = client.post(URL_PREFIX, json=valid_task)
        assert response.status_code == 201
        assert response.json == {'message': 'Task created successfully.'}

def test_create_task_without_title(client):
    body = {
        "description": "Description of Test Task.",
        "status": "In Progress"
    }
    response = client.post(URL_PREFIX, json=body)
    assert response.status_code == 400
    assert response.json == {'error': 'A task must have a title.'}

def test_create_task_with_invalid_status(client, valid_task):
    valid_task['status'] = 'QWERTY'
    response = client.post(URL_PREFIX, json=valid_task)
    assert response.status_code == 400
    posibles_task_states = TaskPhases.get_all_phases()
    message = 'The status of a task only can be:'
    for task_status in posibles_task_states:
        message += f' {task_status},'
    message = message[:-1] + "."
    assert response.json == {'error': message}