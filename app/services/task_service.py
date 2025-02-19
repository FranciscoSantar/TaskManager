from flask import jsonify
from models import Tasks
from data.tasks_phases import TaskPhases
from app.repositories.task_repository import TaskRepository
class TaskService():
    def __init__(self)->None:
        self.model = Tasks
        self.valid_phases = TaskPhases.get_all_phases()

    def get_all(self, page_number:str, items_per_page:str):
        """ Obtain all tasks with a pagination in the response.

        Args:
            page_number (int): Set the page of the task pagination (Default value = 1)
            items_per_page (int): Set the amount of tasks per page (Default value = 10)

        Returns:
            tuple: (Success_get_tasks, message, list[Task])
        """
        check_page_number_type, message = TaskService().check_query_param_type(query_param_name='page number', query_param_value=page_number)
        if not check_page_number_type:
            success = check_page_number_type
            tasks = []
            total_pages = 0
            return success, message, tasks, total_pages
        page_number = int(page_number)
        check_page_number_type, message = self.check_query_param_positive(query_param_name='page number', query_param_value=page_number)
        if not check_page_number_type:
            success = check_page_number_type
            tasks = []
            total_pages = 0
            return success, message, tasks, total_pages

        check_items_per_page_type, message = TaskService().check_query_param_type(query_param_name='items per page', query_param_value=items_per_page)
        if not check_items_per_page_type:
            success = check_items_per_page_type
            tasks = []
            total_pages = 0
            return success, message, tasks, total_pages
        items_per_page = int(items_per_page)
        check_items_per_page_type, message = self.check_query_param_positive(query_param_name='items per page', query_param_value=items_per_page)
        if not check_items_per_page_type:
            success = check_items_per_page_type
            tasks = []
            total_pages = 0
            return success, message, tasks, total_pages
        tasks = TaskRepository().get_all(items_per_page=items_per_page, page_number=page_number)
        success=True
        if not tasks:
            message = 'Tasks not found.'
            total_pages = 0
            return success, message, tasks, total_pages
        total_pages = TaskRepository().get_count_task_pages(page_number=page_number, items_per_page=items_per_page)
        message = 'Tasks found successfully.'
        return success, message, tasks, total_pages

    def get_task_by_id(self, task_id:int):
        """ Obtain a task from a task_id.

        Args:
            task_id (int):
        Returns:
            tuple: (Success_get_task, message, Task)
        """
        check_task_id_type, message = TaskService().check_task_id_type(task_id=task_id)
        if not check_task_id_type:
            return check_task_id_type, message, None

        task_id = int(task_id)
        check_task_id_positive, message = TaskService().check_task_id_positive(task_id=task_id)
        if not check_task_id_positive:
            return check_task_id_positive, message, None

        task = TaskRepository().get_by_id(id=task_id)
        if not task:
            success = True
            message='Task not found.'
            return success, message, {}

        success = True
        message='Task found successfully.'
        return success, message, task

    def create_task(self, title:str, status:str, description:str=None):
        """ Obtain a task and validate new task data.

        Args:
            title(str): This field is required and his max length is 128 characters
            Description(str): This field is optional
            Status(str): This field only can be:
                - To Do (Default value)
                - In Progress
                - Done
        Returns:
            tuple: (Success_create_task, message, Task)
        """
        check_title_exists, message = TaskService().check_exiting_title(title=title)
        if not check_title_exists:
            return check_title_exists, message, None

        check_title_length, message = TaskService().check_title_length(title=title)
        if not check_title_length:
            return check_title_length, message, None

        if status:
            check_status, message = TaskService().check_status(status=status)
            if not check_status:
                return check_status, message, None
        else:
            status = TaskService().set_default_status() #Por defecto, la task se crea con el status To Do

        new_task = TaskRepository().add(title=title, status=status, description=description)
        success = True
        message = 'Task created successfully.'
        return success, message, new_task

    def edit_task(self, task_id:int, title:str=None, status:str=None, description:str=None):
        """ Edit an existing task and validate task data.

        Args:
            title(str): This field is optional. If it's empty, the field doen't change. Max length = 128
            Description(str): This field is optional. If it's empty, the field doen't change
            Status(str):If it's empty, the field doen't change. This field only can be:
                - To Do (Default value)
                - In Progress
                - Done
        Returns:
            tuple: (Success_edit_task, message, Task)
        """
        check_status, message = self.check_status(status=status)
        if not check_status:
            return check_status, message, None

        check_title_length, message = self.check_title_length(title=title)
        if not check_title_length:
            return check_title_length, message, None

        check_get_task_by_id, message, task_to_edit = self.get_task_by_id(task_id=task_id)
        if not task_to_edit:
            return check_get_task_by_id, message, None
        edited_task = TaskRepository().edit(task=task_to_edit, new_title=title, new_status=status, new_description=description)
        success = True
        message = 'Task edited successfully.'
        return success, message, edited_task

    def delete_task(self, task_id:int):
        """ Delete an existing task from a task_id.

        Args:
            task_id (int):
        Returns:
            tuple: (Success_delete_task, message, Task)
        """
        check_get_task_by_id, message, task_to_delete = self.get_task_by_id(task_id=task_id)
        if not task_to_delete:
            return check_get_task_by_id, message, None
        deleted_task = TaskRepository().delete(task=task_to_delete)
        success = True
        message = 'Task deleted successfully.'
        return success, message, deleted_task


    def get_task_phases_string(self) -> str:
        """
        Obtain a string of all possible status of a task.
        """
        message = ""
        for task_status in self.valid_phases:
            message += f' {task_status},'
        message = message[:-1] + "."
        return message

    def check_status(self, status:str):
        """
        Check if the status is valid of all possible task's defined states.
        """
        check_status = self.check_valid_task_phase(status=status)
        if not check_status:
            message = 'The status of a task only can be:' + self.get_task_phases_string()
            return check_status, message
        return check_status, ""

    def check_valid_task_phase(self, status:str) -> bool:
        return status in self.valid_phases

    def check_exiting_title(self, title:str):
        """
        Check if the title of a task is not empty.
        """
        sucess = True
        if not title:
            success = False
            message = 'A task must have a title.'
            return success, message
        return sucess, ""

    def check_title_length(self, title:str):
        """
        Check if the title is too long (Max title length= 128 characters)
        """
        success = True
        if len(title) > 128:
            success = False
            message = 'The title length has to be 128 characters or less.'
            return success, message
        return success, ""

    def set_default_status(self):
        """
        Return the default status of a Task (To Do)
        """
        return TaskPhases.TODO.value

    def check_task_id_type(self, task_id:str):
        """
        Check if the path param task_id is an interger
        """
        success = True
        if not task_id.isdecimal():
            success = False
            message = 'Task ID has to be a number.'
            return success, message
        return success, ""

    def check_query_param_type(self, query_param_value:str, query_param_name:str):
        """
        Check if the selected query param is an interger
        """
        success = True
        if not query_param_value.isdigit():
            success = False
            message = f'Query param: -{query_param_name}- has to be an interger.'
            return success, message
        return success, ""

    def check_task_id_positive(self, task_id:int):
        """
        Check if the path param task_id is a positive number
        """
        success = True
        if task_id <= 0:
            success = False
            message = 'Task ID has to be a positive number.'
            return success, message
        return success, ""

    def check_query_param_positive(self, query_param_value:int, query_param_name:str):
        """
        Check if the selected query param is a positive number
        """
        success = True
        if not query_param_value > 0:
            success = False
            message = f'Query param: -{query_param_name}- has to be a positive number.'
            return success, message
        return success, ""


    def get_response_get_all_tasks(self, success:bool, message:str, total_pages:int, tasks:list['Tasks']):
        """
        Obtain response and status code for get all tasks HTTP request
        """
        if not tasks:
            return jsonify({
                'status': 'success',
                'message': message,
                'data':[],
                'total_pages':0}), 200

        tasks_data = [task.serialize() for task in tasks]
        return jsonify({
            'status': 'success',
            'message': message,
            'data':tasks_data,
            'total_pages':total_pages}), 200

    def get_response_get_task(self, success:bool, message:str, task:Tasks):
        """
        Obtain response and status code for get tasks by task id HTTP request
        """
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

    def get_response_create_task(self, success:bool, message:str, task:Tasks):
        """
        Obtain response and status code for create task HTTP request
        """
        if not success:
            return jsonify({
                'status': 'error',
                'message': message,
                'data':None}), 400

        return jsonify({
            'status': 'success',
            'message': message,
            'data':task.serialize()}), 201

    def get_response_edit_task(self, success:bool, message:str, task:Tasks):
        """
        Obtain response and status code for edit task HTTP request
        """
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

    def get_response_delete_task(self, success:bool, message:str, task:Tasks):
        """
        Obtain response and status code for delete task HTTP request
        """
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
            'data':task.serialize()}), 204

    def get_unexpected_error_response(self):
        """
        Obtain response and status code for unexpected error
        """
        return jsonify({
                "status": "error",
                "message": "An unexpected error occurred. Please try again later."
                }), 500
