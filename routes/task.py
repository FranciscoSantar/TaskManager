from flask import Blueprint, jsonify, request
from controllers.task_controller import TaskController


task_route = Blueprint(name='task_route', import_name=__name__, url_prefix='/task')

@task_route.route('/', methods=['GET'])
def get_all():
    return jsonify({'Sucess':True})

@task_route.route('/<task_id>', methods=['GET'])
def get_task_by_id(task_id):
    sucess, message, task_data = TaskController().get_task_by_id(task_id=task_id)
    if not sucess:
        return jsonify({'error': message}), 400
    if not task_data:
        return jsonify({'task': {}}), 404
    return jsonify({'task': task_data.serialize()}), 200

@task_route.route('/<task_id>', methods=['PUT'])
def edit_task_by_id(task_id):
    data = request.json
    title = data.get('title')
    status = data.get('status')
    description = data.get('description')
    sucess, message, task_data = TaskController().edit_task(task_id=task_id, title=title, status=status, description=description)
    if not sucess:
        return jsonify({'error': message}), 400
    if not task_data:
        return jsonify({'task': {}}), 404
    return jsonify({'task': task_data.serialize()}), 200

@task_route.route('/<task_id>', methods=['DELETE'])
def delete_task_by_id(task_id):
    sucess, message, task_data = TaskController().delete_task(task_id=task_id)
    if not sucess:
        return jsonify({'error': message}), 400
    if not task_data:
        return jsonify({'task': {}}), 404
    return jsonify({'message': 'Task deleted successfully.'}), 204

@task_route.route('/', methods=['POST'])
def create_task():
    data = request.json
    title = data.get('title')
    status = data.get('status')
    description = data.get('description')
    sucess, message = TaskController().create_task(title=title, status=status, description=description)
    if not sucess:
        return jsonify({'error': message}), 400
    return jsonify({'message': message}), 201