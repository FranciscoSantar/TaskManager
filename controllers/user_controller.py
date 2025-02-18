from services.users_service import UsersService, UsersDatabaseService

class UsersController():
    def __init__(self)->None:
        pass

    def register(self, username:str, password:str):
        check_user_information, message = UsersService().check_information(username=username, password=password)
        if not check_user_information:
            user = None
            return check_user_information, message, user
        check_existing_info, message = UsersService().check_existing_user(username=username)
        if not check_existing_info:
            user = None
            return check_existing_info, message, user
        success = True
        created_user = UsersDatabaseService().register(username=username, password=password)
        message = 'User created successfully.'
        return success, message, created_user

