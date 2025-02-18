from . import app, valid_task, db_session
from services.task_service import TaskDatabaseService

def test_create_task_db(db_session, valid_task):
    title = valid_task.get('title')
    status = valid_task.get('status')
    description = valid_task.get('description')
    new_task = TaskDatabaseService().add(title=title, status=status, description=description)

    assert new_task.title == title
    assert new_task.status == status
    assert new_task.description == description