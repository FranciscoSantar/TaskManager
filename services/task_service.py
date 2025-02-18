from models import Tasks
from app import db

class TaskService():
    def __init__(self)->None:
        self.model = Tasks
        pass

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
