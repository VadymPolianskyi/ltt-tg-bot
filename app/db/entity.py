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

    @classmethod
    def default(cls):
        return Category(name="default", user_id=0)


class Activity:
    def __init__(self, name: str, user_id: int, created: datetime = None, id: str = None,
                 category: Category = Category.default()):
        self.id = uuid.uuid4() if id is None else id
        self.name = name
        self.user_id = user_id
        self.created = created
        self.category = category

    @classmethod
    def from_dict(cls, r):
        if 'category_id' in r.keys() and 'category_name' in r.keys():
            category = Category(id=r['category_id'], name=r['category_name'], user_id=r['user_id'])
        else:
            category = Category.default()

        return Activity(id=r['id'], name=r['name'], user_id=r['user_id'], created=r['created'], category=category)


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
    def __init__(self, date: datetime, spent: timedelta, activity_name: str, stop_event_id: str):
        self.date: datetime = date
        self.spent: timedelta = spent
        self.activity_name: str = activity_name
        self.stop_event_id: str = stop_event_id

    @classmethod
    def from_dict(cls, r):
        return EventStatistic(date=r['ev_date'], spent=r['spent'], activity_name=r['activity'],
                              stop_event_id=r['event_id'])
