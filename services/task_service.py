from flask import jsonify
from data.tasks_phases import TaskPhases
from models import Tasks
from app import db

class TaskDatabaseService():
    def __init__(self)->None:
        self.model = Tasks


    def add(self, title:str, status:str, description:str=None) -> Tasks:
        new_task = Tasks(title=title, description=description, status=status)
        db.session.add(new_task)
        db.session.commit()
        return new_task

    def get_by_id(self, id:int) -> Tasks:
        task = db.session.query(self.model).filter_by(id=id).first()
        return task

    def get_all(self):
        return db.session.query(self.model).all()

    def edit(self, task:Tasks, new_title:str, new_status:str, new_description:str) -> Tasks:
        task.title = new_title if new_title else task.title
        task.status = new_status if new_status else task.status
        task.description = new_description if new_description else task.description
        db.session.commit()
        return task

    def delete(self, id:int) -> Tasks:
        task = self.get_by_id(id=id)
        db.session.delete(task)
        db.session.commit()
        return task

class TaskService():
    def __init__(self)->None:
        self.model = Tasks
        self.valid_phases = TaskPhases.get_all_phases()

    def get_task_phases_string(self) -> str:
        message = ""
        for task_status in self.valid_phases:
            message += f' {task_status},'
        message = message[:-1] + "."
        return message

    def check_status(self, status:str):
        check_status = self.check_valid_task_phase(status=status)
        if not check_status:
            message = 'The status of a task only can be:' + self.get_task_phases_string()
            return check_status, message
        return check_status, ""

    def check_valid_task_phase(self, status:str) -> bool:
        return status in self.valid_phases

    def check_exiting_title(self, title:str):
        sucess = True
        if not title:
            success = False
            message = 'A task must have a title.'
            return success, message
        return sucess, ""

    def check_title_length(self, title:str):
        success = True
        if len(title) > 128:
            success = False
            message = 'The title length has to be 128 characters or less.'
            return success, message
        return success, ""

    def set_default_status(self):
        return TaskPhases.TODO.value

    def check_task_id_type(self, task_id:str):
        success = True
        if not task_id.isdecimal():
            success = False
            message = 'Task ID has to be a number.'
            return success, message
        return success, ""

    def check_task_id_positive(self, task_id:int):
        success = True
        if task_id <= 0:
            success = False
            message = 'Task ID has to be a positive number.'
            return success, message
        return success, ""

    def get_response_get_all_tasks(self, success:bool, message:str, tasks:list['Tasks']):
        if not tasks:
            return jsonify({
                'status': 'success',
                'message': message,
                'data':[]}), 200

        tasks_data = [task.serialize() for task in tasks]
        return jsonify({
            'status': 'success',
            'message': message,
            'data':tasks_data}), 200

    def get_response_get_task(self, success:bool, message:str, task:Tasks):
        if not success:
            return jsonify({
                'status': 'error',
                'message': message,
                'data':None}), 400

        if not task:
            return jsonify({
                'status': 'error',
                'message': message,
                'data':{}}), 404

        return jsonify({
            'status': 'success',
            'message': message,
            'data':task.serialize()}), 200

