from flask import Blueprint, jsonify, request
from controllers.task_controller import TaskController
from services.task_service import TaskService

task_router = Blueprint(name='task_route', import_name=__name__, url_prefix='/task')

@task_router.route('/', methods=['GET'])
def get_all():
    success_get_all_tasks, message, tasks = TaskController().get_all()
    response, status_code = TaskService().get_response_get_all_tasks(success=success_get_all_tasks, message=message, tasks=tasks)

    return response, status_code

@task_router.route('/<task_id>', methods=['GET'])
def get_task_by_id(task_id):
    sucess_get_task, message, task_data = TaskController().get_task_by_id(task_id=task_id)
    response, status_code = TaskService().get_response_get_task(success=sucess_get_task, message=message, task=task_data)
    return response, status_code

@task_router.route('/<task_id>', methods=['PUT'])
def edit_task_by_id(task_id):
    data = request.json
    title = data.get('title')
    status = data.get('status')
    description = data.get('description')
    sucess, message, edited_task = TaskController().edit_task(task_id=task_id, title=title, status=status, description=description)
    response, status_code = TaskService().get_response_edit_task(success=sucess, message=message, task=edited_task)
    return response, status_code

@task_router.route('/<task_id>', methods=['DELETE'])
def delete_task_by_id(task_id):
    sucess, message, deleted_task = TaskController().delete_task(task_id=task_id)
    response, status_code = TaskService().get_response_delete_task(success=sucess, message=message, task=deleted_task)
    return response, status_code

@task_router.route('/', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    status = data.get('status')
    description = data.get('description')
    sucess, message, new_task = TaskController().create_task(title=title, status=status, description=description)
    response, status_code = TaskService().get_response_create_task(success=sucess, message=message, task=new_task)
    return response, status_code