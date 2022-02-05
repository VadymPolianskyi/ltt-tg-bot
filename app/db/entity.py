import uuid
from datetime import datetime, timedelta
from enum import Enum


class User:
    def __init__(self, id: int, username: str, time_zone: str = None, created: datetime = None):
        self.id = uuid.uuid4() if id is None else id
        self.username = username
        self.time_zone = time_zone
        self.created = created

    @classmethod
    def from_dict(cls, r):
        return User(id=r['id'], username=r['username'], time_zone=r['time_zone'], created=r['created'])


class Category:
    def __init__(self, name: str, user_id: int, created: datetime = None, id: str = None, ):
        self.id = uuid.uuid4() if id is None else id
        self.name = name
        self.user_id = user_id
        self.created = created

    @classmethod
    def from_dict(cls, r):
        return Category(id=r['id'], name=r['name'], user_id=r['user_id'], created=r['created'])


class Activity:
    def __init__(self, name: str, user_id: int, created: datetime = None, id: str = None,
                 category_id: str = None):
        self.id = str(uuid.uuid4()) if id is None else id
        self.name = name
        self.user_id = user_id
        self.created = created
        self.category_id = category_id

    @classmethod
    def from_dict(cls, r):
        return Activity(id=r['id'], name=r['name'], user_id=r['user_id'], created=r['created'],
                        category_id=r['category_id'])


class EventType(Enum):
    START = 1
    STOP = 2


class Event:
    def __init__(self, activity_id: str, event_type: EventType, user_id: int, time: datetime, id: str = None,
                 last: str = None):
        self.id = uuid.uuid4() if id is None else id
        self.activity_id = activity_id
        self.event_type = event_type
        self.time = time
        self.last = last
        self.user_id = user_id

    @classmethod
    def from_dict(cls, r):
        return Event(id=r['id'], activity_id=r['activity_id'], event_type=r['type'], time=r['time'],
                     user_id=r['user_id'], last=r['last'])


class EventStatistic:
    def __init__(self, date: datetime, spent: timedelta, category_name: str, activity_name: str, stop_event_id: str):
        self.date: datetime = date
        self.spent: timedelta = spent
        self.category_name: str = category_name
        self.activity_name: str = activity_name
        self.stop_event_id: str = stop_event_id

    @classmethod
    def from_dict(cls, r):
        return EventStatistic(date=r['ev_date'],
                              spent=r['spent'],
                              category_name=r['category'],
                              activity_name=r['activity'],
                              stop_event_id=r['event_id']
                              )
