from models import Tasks
from services.task_service import TaskService
from data.tasks_phases import TaskPhases

class TaskController():
    def __init__(self)->None:
        self.valid_phases = TaskPhases.get_all_phases()


    def get_task_phases_string(self) -> str:
        message = ""
        for task_status in self.valid_phases:
            message += f' {task_status},'
        message = message[:-1] + "."
        return message

    def check_valid_task_phase(self, status:str) -> str:
        return status in self.valid_phases

    def get_task_by_id(self, task_id:str) -> Tasks:
        if not task_id.isdecimal():
            success = False
            message = 'Task ID has to be a number.'
            return success, message, None
        task_id = int(task_id)
        if task_id <= 0:
            success = False
            message = 'Task ID has to be a positive number.'
            return success, message, None
        success = True
        task = TaskService().get_by_id(id=task_id)
        task = task if task else None
        return success, None, task

    def edit_task(self, task_id:int, title:str=None, status:str=None, description:str=None) -> Tasks:
        is_status_valid = self.check_valid_task_phase(status=status)
        if status and not is_status_valid:
            success = False
            message = 'The status of a task only can be:'
            message += self.get_task_phases_string()
            return success, message, None
        success, message, task_to_edit = self.get_task_by_id(task_id=task_id)
        if not task_to_edit:
            return success, message, None
        edited_task = TaskService().edit(task=task_to_edit, new_title=title, new_status=status, new_description=description)
        success = True
        return success, None, edited_task


    def create_task(self, title:str, status:str, description:str=None) -> Tasks:
        is_status_valid = self.check_valid_task_phase(status=status)
        if not title:
            success = False
            message = 'A task must have a title.'
            return success, message
        if len(title) > 128:
            success = False
            message = 'The title length has to be 128 characters or less.'
            return success, message
        if not is_status_valid:
            success = False
            message = 'The status of a task only can be:'
            message += self.get_task_phases_string()
            return success, message
        if status is None:
            status = TaskPhases.TODO.value #Por defecto, la task se crea con el status To Do

        new_task = TaskService().add(title=title, status=status, description=description)
        success = True
        message = 'Task created successfully.'
        return success, message
