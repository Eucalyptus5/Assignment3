# calendar_app/user_manager.py
class UserManager:
    _instance = None

    def __init__(self):
        if UserManager._instance is not None:
            raise Exception("This class is a singleton!")
        self.users = {}
        self.next_user_id = 1

    @staticmethod
    def get_instance():
        if UserManager._instance is None:
            UserManager._instance = UserManager()
        return UserManager._instance

    def add_user(self, user):
        self.users[user.user_id] = user

    def get_user_by_id(self, user_id: int):
        return self.users.get(user_id)
    
    def generate_user_id(self):
        uid = self.next_user_id
        self.next_user_id += 1
        return uid