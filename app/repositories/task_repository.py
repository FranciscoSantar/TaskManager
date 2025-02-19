from models import Tasks
from app import db

class TaskRepository():
    def __init__(self)->None:
        self.model = Tasks


    def add(self, title:str, status:str, description:str=None) -> Tasks:
        '''
        This repositoy method create a task in the database.
        '''
        new_task = Tasks(title=title, description=description, status=status)
        db.session.add(new_task)
        db.session.commit()
        return new_task

    def get_by_id(self, id:int) -> Tasks:
        '''
        This repositoy method obtain a task by his id from the database.
        '''
        task = db.session.query(self.model).filter_by(id=id).first()
        return task

    def get_all(self, page_number:int, items_per_page:int):
        '''
        This repositoy method obtain a list of task from the database with pagination params.
        '''
        offset = (page_number-1) * items_per_page
        total_tasks = db.session.query(self.model).count()
        total_pages = total_tasks // items_per_page
        return db.session.query(self.model).offset(offset).limit(items_per_page).all()

    def get_count_task_pages(self, page_number:int, items_per_page:int):
        '''
        This repositoy method obtain the total pages of tasks from pagination params
        '''
        total_tasks = db.session.query(self.model).count()
        total_pages = (total_tasks // items_per_page) + (1 if total_tasks % items_per_page > 0 else 0)
        return total_pages

    def edit(self, task:Tasks, new_title:str, new_status:str, new_description:str) -> Tasks:
        '''
        This repositoy method edit task properties in the database.
        '''
        task.title = new_title if new_title else task.title
        task.status = new_status if new_status else task.status
        task.description = new_description if new_description else task.description
        db.session.commit()
        return task

    def delete(self, task:Tasks) -> Tasks:
        '''
        This repositoy method delete a task from the database.
        '''
        db.session.delete(task)
        db.session.commit()
        return task