from models import Tasks
from services.task_service import TaskService
from data.tasks_phases import TaskPhases

class TaskController():
    def __init__(self)->None:
        pass

    def create_task(self, title:str, status:str, description:str=None) -> Tasks:
        posibles_task_states = TaskPhases.get_all_phases()
        if not title:
            success = False
            message = 'A task must have a title.'
            return success, message
        if len(title) > 128:
            success = False
            message = 'The title length has to be 128 characters or less.'
            return success, message
        if status not in posibles_task_states:
            success = False
            message = 'The status of a task only can be:'
            for task_status in posibles_task_states:
                message += f' {task_status},'
            message = message[:-1] + "."
            return success, message
        if status is None:
            status = TaskPhases.TODO.value #Por defecto, la task se crea con el status To Do

        new_task = TaskService().add(title=title, status=status, description=description)
        success = True
        message = 'Task created successfully.'
        return success, message
