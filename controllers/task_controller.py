from models import Tasks
from services.task_service import TaskService
from data.tasks_phases import TaskPhases

class TaskController():
    def __init__(self)->None:
        self.valid_phases = TaskPhases.get_all_phases()

    def get_all(self, page_number:str, items_per_page:str):
        # try:
            success_get_all_tasks, message, all_tasks, total_pages = TaskService().get_all(items_per_page=items_per_page, page_number=page_number)
            response, status_code = TaskService().get_response_get_all_tasks(success=success_get_all_tasks, message=message, tasks=all_tasks, total_pages=total_pages)
            return response, status_code
        # except Exception:
        #     response, status_code = TaskService().get_unexpected_error_response()
        #     return response, status_code

    def get_task_by_id(self, task_id:str) -> Tasks:
        try:
            success_get_task, message, task = TaskService().get_task_by_id(task_id=task_id)
            response, status_code = TaskService().get_response_get_task(success=success_get_task, message=message, task=task)
            return response, status_code
        except Exception:
            response, status_code = TaskService().get_unexpected_error_response()
            return response, status_code


    def create_task(self, title:str, status:str, description:str=None) -> Tasks:
        try:
            success_create_task, message, created_task = TaskService().create_task(title=title, status=status, description=description)
            response, status_code = TaskService().get_response_edit_task(success=success_create_task, message=message, task=created_task)
            return response, status_code
        except Exception:
            response, status_code = TaskService().get_unexpected_error_response()
            return response, status_code

    def edit_task(self, task_id:int, title:str=None, status:str=None, description:str=None) -> Tasks:
        try:
            success_edit_task, message, edited_task = TaskService().edit_task(task_id=task_id, title=title, status=status, description=description)
            response, status_code = TaskService().get_response_edit_task(success=success_edit_task, message=message, task=edited_task)
            return response, status_code
        except Exception:
            response, status_code = TaskService().get_unexpected_error_response()
            return response, status_code

    def delete_task(self, task_id:str) -> Tasks:
        try:
            success_delete_task, message, deleted_task = TaskService().delete_task(task_id=task_id)
            response, status_code = TaskService().get_response_delete_task(success=success_delete_task, message=message, task=deleted_task)
            return response, status_code
        except Exception:
            response, status_code = TaskService().get_unexpected_error_response()
            return response, status_code
