from app.services.users_service import UsersService

class UsersController():
    def __init__(self)->None:
        pass

    def register(self, username:str, password:str):
        try:
            success_register, message, new_user = UsersService().register(username=username, password=password)
            response, status_code = UsersService().get_response_user_register(success=success_register, message=message, user=new_user)
            return response, status_code
        except Exception:
            response, status_code = UsersService().get_unexpected_error_response()
            return response, status_code

    def login(self, username:str, password:str):
        try:
            success_register, message, token = UsersService().login(username=username, password=password)
            response, status_code = UsersService().get_response_user_login(success=success_register, message=message, token=token)
            return response, status_code
        except Exception:
            response, status_code = UsersService().get_unexpected_error_response()
            return response, status_code
