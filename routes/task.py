from flask import Blueprint, jsonify

task_route = Blueprint(name='task_route', import_name=__name__, url_prefix='/task')

@task_route.route('/', methods=['GET'])
def ping():
    return jsonify({'Sucess':True})