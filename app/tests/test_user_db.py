from app.tests import app, valid_user, db_session
from app.repositories.users_repository import UsersRepository
from werkzeug.security import check_password_hash
from models import Users

def test_register_user_db(db_session, valid_user):
    username = valid_user.get('username')
    password = valid_user.get('password')
    new_user = UsersRepository().register(username=username, password=password)
    assert new_user.username == username
    assert new_user.password != password
    assert isinstance(new_user, Users)
    assert check_password_hash(new_user.password, password) == True

def test_get_user_by_username(db_session, valid_user):
    username = valid_user.get('username')
    password = valid_user.get('password')
    existing_user = UsersRepository().get_user_by_username(username=username)
    assert existing_user is None
    new_user = UsersRepository().register(username=username, password=password)
    existing_user = UsersRepository().get_user_by_username(username=username)
    assert existing_user.username == username
    assert existing_user.password != password
    assert isinstance(existing_user, Users)
    assert check_password_hash(existing_user.password, password) == True