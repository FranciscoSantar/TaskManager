from tests.utils import format_date_in_response
from . import valid_task, app, client, valid_task_object, valid_task_serialize, valid_list_of_task_objects, valid_list_of_task_objects_serialize
from unittest.mock import patch
from controllers.task_controller import TaskController
from services.task_service import TaskService
from datetime import datetime

URL_PREFIX = '/task'



### CREATE TASK TESTS



def test_create_valid_task(client, valid_task, valid_task_object, valid_task_serialize):
    with patch.object(TaskController, 'create_task', return_value=(True, 'Task created successfully.', valid_task_object)):
        response = client.post(f"{URL_PREFIX}/", json=valid_task)
        response_data = format_date_in_response(response=response)
        assert response.status_code == 201
        assert response_data == {
                                    'status': 'success',
                                    'message': 'Task created successfully.',
                                    'data': valid_task_serialize
                                }

def test_create_task_without_title(client):
    body = {
        "description": "Description of Test Task.",
        "status": "In Progress"
    }
    response = client.post(f"{URL_PREFIX}/", json=body)
    assert response.status_code == 400
    assert response.json == {
                                'status': 'error',
                                'message': 'A task must have a title.',
                                'data':None
                            }

def test_create_task_with_invalid_status(client, valid_task):
    valid_task['status'] = 'QWERTY'
    response = client.post(f"{URL_PREFIX}/", json=valid_task)
    message = 'The status of a task only can be:'
    message += TaskService().get_task_phases_string()
    assert response.status_code == 400
    assert response.json == {
                                'status': 'error',
                                'message': message,
                                'data':None
                            }



### GET TASK BY ID TESTS



def test_get_task_by_valid_id(client, valid_task_serialize, valid_task_object):
    with patch.object(TaskController, 'get_task_by_id', return_value=(True, 'Task found successfully.', valid_task_object)):
        response = client.get(f"{URL_PREFIX}/1")
        response_data = format_date_in_response(response=response)
        assert response.status_code == 200
        assert response_data == {
                                'status': 'success',
                                'message': 'Task found successfully.',
                                'data':valid_task_serialize
                                }

def test_get_not_existing_task(client):
    with patch.object(TaskController, 'get_task_by_id', return_value=(True, 'Task not found.', {})):
        response = client.get(f"{URL_PREFIX}/1")
        assert response.status_code == 404
        assert response.json == {
                'status': 'error',
                'message': 'Task not found.',
                'data':{}}

def test_get_task_by_alphabetic_id(client):
    response = client.get(f"{URL_PREFIX}/qwerty1")
    assert response.status_code == 400
    assert response.json == {
                'status': 'error',
                'message': 'Task ID has to be a number.',
                'data':None}

def test_get_task_by_zero_id(client):
    response = client.get(f"{URL_PREFIX}/0")
    assert response.status_code == 400
    assert response.json ==  {
                'status': 'error',
                'message': 'Task ID has to be a positive number.',
                'data':None}


### GET ALL TASKS TESTS



def test_get_all_valid_tasks(client, valid_list_of_task_objects_serialize, valid_list_of_task_objects):
    with patch.object(TaskController, 'get_all', return_value=(True, 'Tasks found successfully.', valid_list_of_task_objects)):
        response = client.get(f"{URL_PREFIX}/")
        response_data = format_date_in_response(response=response)
        assert response.status_code == 200
        assert response_data == {
                'status': 'success',
                'message': 'Tasks found successfully.',
                'data':valid_list_of_task_objects_serialize}

def test_get_all_not_existing_task(client):
    with patch.object(TaskController, 'get_all', return_value=(True, 'Tasks not found.', [])):
        response = client.get(f"{URL_PREFIX}/")
        assert response.status_code == 200
        assert response.json == {
                'status': 'success',
                'message': 'Tasks not found.',
                'data':[]}



### EDIT TASK BY ID TESTS



def test_edit_task_by_valid_id(client, valid_task_serialize, valid_task_object, valid_task):
    with patch.object(TaskController, 'edit_task', return_value=(True, 'Task edited successfully.', valid_task_object)):
        response = client.put(f"{URL_PREFIX}/1", json=valid_task)
        response_data = format_date_in_response(response=response)
        assert response.status_code == 200
        assert response_data == {
                                    'status': 'success',
                                    'message': 'Task edited successfully.',
                                    'data':valid_task_serialize
                                }

def test_edit_not_existing_task(client, valid_task):
    with patch.object(TaskController, 'edit_task', return_value=(True, 'Task not found.', {})):
        response = client.put(f"{URL_PREFIX}/1", json=valid_task)
        assert response.status_code == 404
        assert response.json == {
                                    'status': 'error',
                                    'message': 'Task not found.',
                                    'data':{}
                                }

def test_edit_task_by_alphabetic_id(client, valid_task):
    response = client.put(f"{URL_PREFIX}/qwerty1", json=valid_task)
    assert response.status_code == 400
    assert response.json == {
                                'status': 'error',
                                'message': 'Task ID has to be a number.',
                                'data':None
                            }

def test_edit_task_by_zero_id(client, valid_task):
    response = client.put(f"{URL_PREFIX}/0", json=valid_task)
    assert response.status_code == 400
    assert response.json == {
                                'status': 'error',
                                'message': 'Task ID has to be a positive number.',
                                'data':None
                            }

def test_edit_task_with_invalid_status(client, valid_task):
    valid_task['status'] = 'QWERTY'
    response = client.put(f"{URL_PREFIX}/1", json=valid_task)
    message = 'The status of a task only can be:'
    message += TaskService().get_task_phases_string()
    assert response.status_code == 400
    assert response.json == {
                                'status': 'error',
                                'message': message,
                                'data':None
                            }



### DELETE TASK BY ID TESTS



def test_delete_task_by_valid_id(client, valid_task_object):
    with patch.object(TaskController, 'delete_task', return_value=(True, 'Task deleted successfully.', valid_task_object)):
        response = client.delete(f"{URL_PREFIX}/1")
        assert response.status_code == 204

def test_delete_not_existing_task(client):
    with patch.object(TaskController, 'delete_task', return_value=(True, 'Task not found.', {})):
        response = client.delete(f"{URL_PREFIX}/1")
        assert response.status_code == 404
        assert response.json == {
                                    'status': 'error',
                                    'message': 'Task not found.',
                                    'data':{}
                                }

def test_delete_task_by_alphabetic_id(client):
    response = client.delete(f"{URL_PREFIX}/qwerty1")
    assert response.status_code == 400
    assert response.json == {
                                'status': 'error',
                                'message': 'Task ID has to be a number.',
                                'data':None
                            }

def test_delete_task_by_zero_id(client):
    response = client.delete(f"{URL_PREFIX}/0")
    assert response.status_code == 400
    assert response.json == {
                                'status': 'error',
                                'message': 'Task ID has to be a positive number.',
                                'data':None
                            }