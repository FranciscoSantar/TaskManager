from models import Tasks
from app.services.task_service import TaskService
from data.tasks_phases import TaskPhases
import redis
import json
from app.logger import logger
from flask import jsonify

r = redis.Redis(host='redis-container', port=6379, decode_responses=True)

class TaskController():
    def __init__(self)->None:
        self.valid_phases = TaskPhases.get_all_phases()

    def get_all(self, page_number:str, items_per_page:str):
        '''
            This controller obtain all tasks.
        '''
        try:
            response, status_code = self.check_all_tasks_cache(page_number=page_number, items_per_page=items_per_page)
            return response, status_code
        except Exception:
            response, status_code = TaskService().get_unexpected_error_response()
            return response, status_code

    def get_task_by_id(self, task_id:str) -> Tasks:
        '''
            This controller obtain the task data from the task id path param indicated
        '''
        try:
            response, status_code = self.check_task_by_id_cache(task_id=task_id)
            return response, status_code
        except Exception:
            response, status_code = TaskService().get_unexpected_error_response()
            return response, status_code


    def create_task(self, title:str, status:str, description:str=None) -> Tasks:
        '''
            This controller create a task from a body of task properties:
            - title:str = This field is required and his max length is 128 characters
            - Description:str = This field is optional
            - Status:str = This field only can be:
                - To Do (Default value)
                - In Progress
                - Done
        '''
        try:
            success_create_task, message, created_task = TaskService().create_task(title=title, status=status, description=description)
            response, status_code = TaskService().get_response_edit_task(success=success_create_task, message=message, task=created_task)
            self.clear_all_tasks_cache()
            return response, status_code
        except Exception:
            response, status_code = TaskService().get_unexpected_error_response()
            return response, status_code

    def edit_task(self, task_id:int, title:str=None, status:str=None, description:str=None) -> Tasks:
        '''
            This controller edit  an existing task:
            - title:str = This field is optional. If it's empty, the field doen't change
            - Description:str = This field is optional. If it's empty, the field doen't change
            - Status:str = . If it's empty, the field doen't change. This field only can be:
                - To Do (Default value)
                - In Progress
                - Done
        '''
        try:
            success_edit_task, message, edited_task = TaskService().edit_task(task_id=task_id, title=title, status=status, description=description)
            response, status_code = TaskService().get_response_edit_task(success=success_edit_task, message=message, task=edited_task)
            self.clear_task_cache(task_id=task_id)
            return response, status_code
        except Exception:
            response, status_code = TaskService().get_unexpected_error_response()
            return response, status_code

    def delete_task(self, task_id:str) -> Tasks:
        '''
            This controller delete a task from the task id path param indicated
        '''
        try:
            success_delete_task, message, deleted_task = TaskService().delete_task(task_id=task_id)
            response, status_code = TaskService().get_response_delete_task(success=success_delete_task, message=message, task=deleted_task)
            return response, status_code
        except Exception:
            response, status_code = TaskService().get_unexpected_error_response()
            return response, status_code

    def clear_all_tasks_cache(self):
        '''
            Clear get all task cache when a new task is created
        '''
        keys_to_delete = r.scan_iter("get_all_*")
        for key in keys_to_delete:
            r.delete(key)
        logger.info("Caché de 'get_all_*' eliminada")

    def clear_task_cache(self,task_id):
        '''
            Clear a task cache when a this one is updated.
        '''
        keys_to_delete = r.scan_iter(f"get_task_id_{task_id}")
        for key in keys_to_delete:
            r.delete(key)
        logger.info(f"Caché de 'get_task_id_{task_id}' eliminada")

    def check_all_tasks_cache(self, page_number:str, items_per_page:str):
        '''
            Check if all_tasks data is storage in cache, if not, storage it on
        '''
        key_name = f"get_all_tasks_page_{page_number}_items_{items_per_page}"
        if r.exists(key_name):
            data = r.get(key_name)
            response_dict, status_code = json.loads(data)
            response = jsonify(response_dict)
        else:
            success_get_all_tasks, message, all_tasks, total_pages = TaskService().get_all(items_per_page=items_per_page, page_number=page_number)
            response, status_code = TaskService().get_response_get_all_tasks(success=success_get_all_tasks, message=message, tasks=all_tasks, total_pages=total_pages)
            response_data = response.json
            if status_code < 300:
                r.setex(key_name, 100, json.dumps((response_data, status_code)))
        return response, status_code

    def check_task_by_id_cache(self, task_id:int):
        '''
            Check if a task data is storage in cache, if not, storage on it
        '''
        key_name = f"get_task_id_{task_id}"
        if r.exists(key_name):
            data = r.get(key_name)
            response_dict, status_code = json.loads(data)
            response = jsonify(response_dict)
        else:
            success_get_task, message, task = TaskService().get_task_by_id(task_id=task_id)
            response, status_code = TaskService().get_response_get_task(success=success_get_task, message=message, task=task)
            response_data = response.json
            if status_code < 300:
                r.setex(key_name, 100, json.dumps((response_data, status_code)))
        return response, status_code
