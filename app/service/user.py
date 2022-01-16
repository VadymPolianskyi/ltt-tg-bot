from app.db.dao import UserDao
from app.db.entity import Activity, User


# todo: add caching for timezone
class UserService:
    DEFAULT_TIMEZONE = "UTC"

    def __init__(self):
        self.dao = UserDao()

    def create(self, user_id: int, username: str, timezone: str) -> Activity:
        print(f"Create User(id={user_id}, username={username}, timezone={timezone})")
        u = User(id=user_id, username=username, time_zone=timezone)
        self.dao.save(u)
        return u

    def get_time_zone(self, user_id: int) -> str:
        print(f'Get Time Zone for User({user_id})')
        u = self.dao.find(user_id)
        user_time_zone = u.time_zone if u else self.DEFAULT_TIMEZONE
        print(f'User({user_id}) time zone is {user_time_zone}')
        return user_time_zone

    def update_time_zone(self, user_id: int, time_zone: str):
        print(f'Update Time Zone for User({user_id})')
        if self.dao.find(user_id):
            self.dao.update_time_zone(user_id, time_zone)
        else:
            print(f'User({user_id}) not found for updating time zone.')
            self.create(user_id, "", time_zone)
