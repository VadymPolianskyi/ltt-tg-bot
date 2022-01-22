from app.config import msg
from app.db.dao import ActivityDao, EventDao
from app.db.entity import Activity
from app.service import markup


class ActivityService:
    def __init__(self):
        self.dao = ActivityDao()
        self.event_dao = EventDao()

    def create(self, user_id: int, activity_name: str, category_id: str) -> Activity:
        print(f"Create Activity({activity_name}) in Category({category_id}) for User({str(user_id)})")
        a = Activity(user_id=user_id, name=activity_name, category_id=category_id)
        self.dao.save(a)
        return a

    def delete(self, activity_id: str):
        print(f"Delete Activity({activity_id})")
        self.event_dao.delete_all_for_activity(activity_id)
        self.dao.delete(activity_id)

    def all_started_activities(self, user_id: int) -> list:
        print(f"Find all started activities for user({str(user_id)})")
        started_activities = self.dao.find_last_started(user_id)
        print(f'Found {len(started_activities)} started activities for user({str(user_id)})')
        return started_activities

    def find(self, activity_id: str) -> Activity:
        print(f"Find Activity({activity_id})")
        return self.dao.find(activity_id)

    def all(self, category_id: str) -> list:
        print(f"Find all activities for Category({category_id})")
        activities = self.dao.find_all_by_category(category_id)
        print(f"Found {len(activities)} activities for Category({category_id})")
        return activities

    def update(self, activity: Activity):
        print(f"Update Activity({activity.id}) for User({activity.user_id})")
        self.dao.update(activity)

    def create_all_activities_markup(self, marker: str, category_id: str, back_button_marker: str):
        buttons = [(a.name, marker, a.id) for a in self.all(category_id)]
        buttons.append((msg.BACK_BUTTON, back_button_marker, '_'))
        return markup.create_inline_markup_(buttons)

    # migration
    def migrate(self, user_id: int, default_category_id: str):
        activities_without_category = [a for a in self.dao.find_all_by_user_id(user_id) if a.category_id is None]

        for a in activities_without_category:
            a.category_id = default_category_id
            self.update(a)
