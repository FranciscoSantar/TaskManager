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

def test_edit_task_db(db_session, valid_task):
    title = valid_task.get('title')
    status = valid_task.get('status')
    description = valid_task.get('description')
    new_task = TaskDatabaseService().add(title=title, status=status, description=description)
    new_title = 'New title'
    new_status = 'New status'
    new_description = 'New description'
    edited_task = TaskDatabaseService().edit(task=new_task, new_title=new_title, new_description=new_description, new_status=new_status)

    assert new_task.title != title
    assert new_task.status != status
    assert new_task.description != description
    assert new_task.title == new_title
    assert new_task.status == new_status
    assert new_task.description == new_description

def test_delete_task_db(db_session, valid_task):
    title = valid_task.get('title')
    status = valid_task.get('status')
    description = valid_task.get('description')
    new_task = TaskDatabaseService().add(title=title, status=status, description=description)

    deleted_task = TaskDatabaseService().delete(task=new_task)

    get_deleted_task = TaskDatabaseService().get_by_id(id=new_task.id)
    assert get_deleted_task is None