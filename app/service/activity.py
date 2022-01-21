from app.db.dao import ActivityDao, EventDao
from app.db.entity import Activity
from app.service import markup


class ActivityService:
    def __init__(self):
        self.dao = ActivityDao()
        self.event_dao = EventDao()

    def create(self, user_id: int, activity_name: str) -> Activity:
        print(f"Create activity({activity_name}) for user({str(user_id)})")
        a = Activity(user_id=user_id, name=activity_name)
        self.dao.save(a)
        return a

    def delete(self, user_id: int, activity_name: str):
        print(f"Delete all  activity({activity_name}) events for user({str(user_id)})")
        a = self.dao.find_by_user_id_and_name(user_id, activity_name)
        self.event_dao.delete_all_for_activity(a.id)
        self.dao.delete(user_id, a.name)

    def show_all(self, user_id: int) -> list:
        print(f"Show all activities for user({str(user_id)})")
        return self.dao.find_all_by_user_id(user_id)

    def show_all_titles(self, user_id: int) -> list:
        print(f"Show all titles for user({str(user_id)})")
        return [a.name for a in self.show_all(user_id)]

    def all_activities_keyboard(self, user_id: int, key: str):
        all_user_activity_titles = self.show_all_titles(user_id)
        return markup.create_simple_inline_markup(key, all_user_activity_titles)

    def all_started_activity_titles(self, user_id: int) -> list:
        print(f"Find last started activities for user({str(user_id)})")
        started_activities = self.dao.find_last_started(user_id)
        print(f'Found {len(started_activities)} started activities for user({str(user_id)})')
        return [a.name for a in started_activities]

    def find_all(self, category_id: str) -> list:
        print(f"Find all activities for Category({category_id})")
        activities = self.dao.find_all_by_categoty_id(category_id)
        print(f"Found {len(activities)} activities for Category({category_id})")
        return activities
