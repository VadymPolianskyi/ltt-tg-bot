from datetime import datetime
from typing import Optional

from app.db.dao import ActivityDao, EventDao
from app.db.entity import EventType, Event
from app.service import time_service


class EventService:
    def __init__(self):
        self.dao = EventDao()
        self.activity_dao = ActivityDao()

    def create(self, user_id: int, activity_id: str, event_type: EventType, time: datetime, last: str = None) -> Event:
        if not last:
            last_event = self.find_last(activity_id, EventType.STOP)
            last = "first" if not last_event else last_event.id
        e = Event(activity_id=activity_id, event_type=event_type, time=time, last=last, user_id=user_id)
        self.dao.save(e)
        print(f'Created Event({e.id}, {e.event_type})')
        return e

    def find_last(self, activity_id: str, event_type: EventType) -> Optional[Event]:
        return self.dao.find_last_event_for_activity(activity_id, event_type)

    def delete_pair(self, stop_event_id: str):
        start_event_id = self.dao.find(stop_event_id).last
        self.dao.delete(start_event_id, stop_event_id)

    def delete(self, *event_ids):
        self.dao.delete(*event_ids)

    def finish_and_calculate_time(self, user_id: int, activity_id: str, time: datetime) -> tuple:
        print(f"Finish event for Activity({activity_id})")
        e_start = self.find_last(activity_id, EventType.START)
        e_stop = self.create(
            user_id=user_id,
            activity_id=activity_id,
            event_type=EventType.STOP,
            time=time,
            last=e_start.id
        )

        hours, minutes = time_service.count_difference(e_start.time, e_stop.time)
        return hours, minutes

    def find(self, event_id: str):
        print(f'Find Event({event_id})')
        return self.dao.find(event_id)
