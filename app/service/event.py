from datetime import datetime
from typing import Optional

from app.db.dao import ActivityDao, EventDao
from app.db.entity import EventType, Event


class EventService:
    def __init__(self):
        self.dao = EventDao()
        self.activity_dao = ActivityDao()

    def create(self, user_id: int, activity_name: str, event_type: EventType, time: datetime,
               last: str = None) -> Event:
        a = self.activity_dao.find_by_user_id_and_name(user_id, activity_name)
        if not last:
            last_event = self.find_last(user_id, activity_name, EventType.STOP)
            last = "first" if not last_event else last_event.id
        e = Event(activity_id=a.id, event_type=event_type, time=time, last=last, user_id=user_id)
        self.dao.save(e)
        print(f'Created {e}')
        return e

    def find_last(self, user_id: int, activity_name: str, event_type: EventType) -> Optional[Event]:
        return self.dao.find_last_event_for_activity(user_id, activity_name, event_type)

    def delete_pair(self, stop_event_id: str):
        start_event_id = self.dao.find(stop_event_id).last
        self.dao.delete(start_event_id, stop_event_id)

    def delete(self, *event_ids):
        self.dao.delete(*event_ids)
