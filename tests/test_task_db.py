from . import app, valid_task, db_session
from repositories.task_repository import TaskRepository
from models import Tasks

def test_create_task_db(db_session, valid_task):
    title = valid_task.get('title')
    status = valid_task.get('status')
    description = valid_task.get('description')
    new_task = TaskRepository().add(title=title, status=status, description=description)

    assert new_task.title == title
    assert new_task.status == status
    assert new_task.description == description

    get_new_task = TaskRepository().get_by_id(id=new_task.id)

    assert isinstance(get_new_task, Tasks) == True
    assert get_new_task.title == title
    assert get_new_task.status == status
    assert get_new_task.description == description

def test_edit_task_db(db_session, valid_task):
    title = valid_task.get('title')
    status = valid_task.get('status')
    description = valid_task.get('description')
    new_task = TaskRepository().add(title=title, status=status, description=description)
    new_title = 'New title'
    new_status = 'New status'
    new_description = 'New description'
    edited_task = TaskRepository().edit(task=new_task, new_title=new_title, new_description=new_description, new_status=new_status)

    assert new_task.title != title
    assert new_task.status != status
    assert new_task.description != description
    assert new_task.title == new_title
    assert new_task.status == new_status
    assert new_task.description == new_description

    get_edited_task = TaskRepository().get_by_id(id=edited_task.id)

    assert isinstance(get_edited_task, Tasks) == True
    assert get_edited_task.title == new_title
    assert get_edited_task.status == new_status
    assert get_edited_task.description == new_description

def test_delete_task_db(db_session, valid_task):
    title = valid_task.get('title')
    status = valid_task.get('status')
    description = valid_task.get('description')
    new_task = TaskRepository().add(title=title, status=status, description=description)

    assert new_task.title == title
    assert new_task.status == status
    assert new_task.description == description

    deleted_task = TaskRepository().delete(task=new_task)

    get_deleted_task = TaskRepository().get_by_id(id=new_task.id)
    assert get_deleted_task is None