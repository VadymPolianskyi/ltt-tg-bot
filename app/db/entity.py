import uuid
from datetime import datetime, timedelta
from enum import Enum


class User:
    def __init__(self, id: int, username: str, timezone: str = None, created: datetime = None):
        self.id = id
        self.username = username
        self.timezone = timezone
        self.created = created


class Activity:
    def __init__(self, name: str, user_id: int, created: datetime = None, id: str = None, ):
        self.name = name
        self.user_id = user_id
        self.id = uuid.uuid4() if id is None else id
        self.created = created


class EventType(Enum):
    START = 1
    STOP = 2


class Event:
    def __init__(self, activity_id: str, event_type: EventType, user_id: int, id: str = None, last: str = None,
                 time: datetime = None):
        self.id = uuid.uuid4() if id is None else id
        self.activity_id = activity_id
        self.event_type = event_type
        self.time = datetime.now() if time is None else time
        self.last = last
        self.user_id = user_id


class EventStatistic:
    def __init__(self, date: datetime, spent: timedelta, activity_name: str, stop_event_id: str):
        self.date: datetime = date
        self.spent: timedelta = spent
        self.activity_name: str = activity_name
        self.stop_event_id: str = stop_event_id
