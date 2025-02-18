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
