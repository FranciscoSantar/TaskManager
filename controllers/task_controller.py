from models import Tasks
from services.task_service import TaskDatabaseService, TaskService
from data.tasks_phases import TaskPhases
from flask import jsonify

class TaskController():
    def __init__(self)->None:
        self.valid_phases = TaskPhases.get_all_phases()

    def get_all(self):
        tasks = TaskDatabaseService().get_all()
        success=True
        if not tasks:
            message = 'Tasks not found.'
            return success, message, tasks

        message = 'Tasks found successfully.'
        return success, message, tasks

    def get_task_by_id(self, task_id:str) -> Tasks:
        check_task_id_type, message = TaskService().check_task_id_type(task_id=task_id)
        if not check_task_id_type:
            return check_task_id_type, message, None

        task_id = int(task_id)

        check_task_id_positive, message = TaskService().check_task_id_positive(task_id=task_id)
        if not check_task_id_positive:
            return check_task_id_positive, message, None

        task = TaskDatabaseService().get_by_id(id=task_id)
        if not task:
            success = True
            message='Task not found.'
            return success, message, task
        success = True
        message='Task found successfully.'
        return success, message, task


    def create_task(self, title:str, status:str, description:str=None) -> Tasks:
        check_title_exists, message = TaskService().check_exiting_title(title=title)
        if not check_title_exists:
            return check_title_exists, message

        check_title_length, message = TaskService().check_title_length(title=title)
        if not check_title_length:
            return check_title_length, message

        check_status, message = TaskService().check_status(status=status)
        if not check_status:
            return check_status, message

        if status is None:
            status = TaskService().set_default_status() #Por defecto, la task se crea con el status To Do

        new_task = TaskDatabaseService().add(title=title, status=status, description=description)
        success = True
        message = 'Task created successfully.'
        return success, message

    def edit_task(self, task_id:int, title:str=None, status:str=None, description:str=None) -> Tasks:
        check_status, message = TaskService().check_status(status=status)
        if not check_status:
            return check_status, message, None

        check_get_task_by_id, message, task_to_edit = self.get_task_by_id(task_id=task_id)
        if not task_to_edit:
            return check_get_task_by_id, message, None
        edited_task = TaskDatabaseService().edit(task=task_to_edit, new_title=title, new_status=status, new_description=description)
        success = True
        return success, None, edited_task

    def delete_task(self, task_id:str) -> Tasks:
        check_get_task_by_id, message, task_to_delete = self.get_task_by_id(task_id=task_id)
        if not task_to_delete:
            return check_get_task_by_id, message, None
        deleted_task = TaskDatabaseService().delete(id=task_id)
        success = True
        return success, None, deleted_task
