from . import valid_task, app, client, valid_task_object, valid_task_serialize, valid_list_of_task_objects, valid_list_of_task_objects_serialize
from unittest.mock import patch
from controllers.task_controller import TaskController
from datetime import datetime

URL_PREFIX = '/task'



### CREATE TASK TESTS



def test_create_valid_task(client, valid_task):
    with patch.object(TaskController, 'create_task', return_value=(True, "Task created successfully.")):
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
    message = 'The status of a task only can be:'
    message += TaskController().get_task_phases_string()
    assert response.status_code == 400
    assert response.json == {'error': message}



### GET TASK BY ID TESTS



def test_get_task_by_valid_id(client, valid_task_serialize, valid_task_object):
    with patch.object(TaskController, 'get_task_by_id', return_value=(True, None, valid_task_object)):
        response = client.get(f"{URL_PREFIX}/1")
        response_data = response.json['task']
        for key in ['created_at', 'updated_at']:
            response_data[key] = datetime.strptime(response_data[key], '%a, %d %b %Y %H:%M:%S GMT')
        assert response.status_code == 200
        assert response_data == valid_task_serialize

def test_get_not_existing_task(client):
    with patch.object(TaskController, 'get_task_by_id', return_value=(True, None, None)):
        response = client.get(f"{URL_PREFIX}/1")
        response_data = response.json['task']
        assert response.status_code == 404
        assert response_data == {}

def test_get_task_by_alphabetic_id(client):
    response = client.get(f"{URL_PREFIX}/qwerty1")
    assert response.status_code == 400
    assert response.json == {'error': 'Task ID has to be a number.'}

def test_get_task_by_zero_id(client):
    response = client.get(f"{URL_PREFIX}/0")
    assert response.status_code == 400
    assert response.json == {'error': 'Task ID has to be a positive number.'}


### GET ALL TASKS TESTS



def test_get_all_valid_tasks(client, valid_list_of_task_objects_serialize, valid_list_of_task_objects):
    with patch.object(TaskController, 'get_all', return_value=(valid_list_of_task_objects)):
        response = client.get(f"{URL_PREFIX}/")
        response_data = response.json['tasks']
        for data_task in response_data:
            for key in ['created_at', 'updated_at']:
                data_task[key] = datetime.strptime(data_task[key], '%a, %d %b %Y %H:%M:%S GMT')
        assert response.status_code == 200
        assert response_data == valid_list_of_task_objects_serialize

def test_get_all_not_existing_task(client):
    with patch.object(TaskController, 'get_all', return_value=([])):
        response = client.get(f"{URL_PREFIX}/")
        response_data = response.json['tasks']
        assert response.status_code == 404
        assert response_data == []



### EDIT TASK BY ID TESTS



def test_edit_task_by_valid_id(client, valid_task_serialize, valid_task_object, valid_task):
    with patch.object(TaskController, 'edit_task', return_value=(True, None, valid_task_object)):
        response = client.put(f"{URL_PREFIX}/1", json=valid_task)
        response_data = response.json['task']
        for key in ['created_at', 'updated_at']:
            response_data[key] = datetime.strptime(response_data[key], '%a, %d %b %Y %H:%M:%S GMT')
        assert response.status_code == 200
        assert response_data == valid_task_serialize

def test_edit_not_existing_task(client, valid_task):
    with patch.object(TaskController, 'edit_task', return_value=(True, None, None)):
        response = client.put(f"{URL_PREFIX}/1", json=valid_task)
        response_data = response.json['task']
        assert response.status_code == 404
        assert response_data == {}

def test_edit_task_by_alphabetic_id(client, valid_task):
    response = client.put(f"{URL_PREFIX}/qwerty1", json=valid_task)
    assert response.status_code == 400
    assert response.json == {'error': 'Task ID has to be a number.'}

def test_edit_task_by_zero_id(client, valid_task):
    response = client.put(f"{URL_PREFIX}/0", json=valid_task)
    assert response.status_code == 400
    assert response.json == {'error': 'Task ID has to be a positive number.'}

def test_edit_task_with_invalid_status(client, valid_task):
    valid_task['status'] = 'QWERTY'
    response = client.put(f"{URL_PREFIX}/1", json=valid_task)
    message = 'The status of a task only can be:'
    message += TaskController().get_task_phases_string()
    assert response.status_code == 400
    assert response.json == {'error': message}



### DELETE TASK BY ID TESTS



def test_delete_task_by_valid_id(client, valid_task_object):
    with patch.object(TaskController, 'delete_task', return_value=(True, None, valid_task_object)):
        response = client.delete(f"{URL_PREFIX}/1")
        assert response.status_code == 204

def test_delete_not_existing_task(client):
    with patch.object(TaskController, 'delete_task', return_value=(True, None, None)):
        response = client.delete(f"{URL_PREFIX}/1")
        response_data = response.json['task']
        assert response.status_code == 404
        assert response_data == {}

def test_delete_task_by_alphabetic_id(client):
    response = client.delete(f"{URL_PREFIX}/qwerty1")
    assert response.status_code == 400
    assert response.json == {'error': 'Task ID has to be a number.'}

def test_delete_task_by_zero_id(client):
    response = client.delete(f"{URL_PREFIX}/0")
    assert response.status_code == 400
    assert response.json == {'error': 'Task ID has to be a positive number.'}