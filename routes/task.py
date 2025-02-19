from flask import Blueprint, jsonify, request
from controllers.task_controller import TaskController
from flask_jwt_extended import jwt_required
from services.task_service import TaskService

task_router = Blueprint(name='task_route', import_name=__name__, url_prefix='/task')

@task_router.route('/', methods=['GET'])
@jwt_required()
def get_all():
    items_per_page = request.args.get('items-per-page', '10')
    page_number = request.args.get('page-number', '1')
    response, status_code = TaskController().get_all(items_per_page=items_per_page, page_number=page_number)
    return response, status_code

@task_router.route('/<task_id>', methods=['GET'])
@jwt_required()
def get_task_by_id(task_id):
    response, status_code = TaskController().get_task_by_id(task_id=task_id)
    return response, status_code

@task_router.route('/<task_id>', methods=['PUT'])
@jwt_required()
def edit_task_by_id(task_id):
    data = request.json
    title = data.get('title')
    status = data.get('status')
    description = data.get('description')
    response, status_code = TaskController().edit_task(task_id=task_id, title=title, status=status, description=description)
    return response, status_code

@task_router.route('/<task_id>', methods=['DELETE'])
@jwt_required()
def delete_task_by_id(task_id):
    response, status_code = TaskController().delete_task(task_id=task_id)
    return response, status_code

@task_router.route('/', methods=['POST'])
@jwt_required()
def create_task():
    data = request.json
    title = data.get('title')
    status = data.get('status')
    description = data.get('description')
    response, status_code = TaskController().create_task(title=title, status=status, description=description)
    return response, status_code