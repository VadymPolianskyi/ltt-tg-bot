from datetime import datetime
from typing import Optional

import app.util.time as time
from app.db import ActivityDao, Activity, EventDao, EventType, Event
from app.statistics import FullStatistics, ActivityStatistics


class ActivityService:
    def __init__(self):
        self.dao = ActivityDao()
        self.event_dao = EventDao()

    def create(self, username: str, activity_name: str) -> Activity:
        a = Activity(username=username, name=activity_name)
        self.dao.save(a)
        return a

    def delete(self, username: str, activity_name: str):
        a = self.dao.find_by_username_and_name(username, activity_name)
        self.event_dao.delete_all_by_activity(username, a.id)
        self.dao.delete(username, activity_name)

    def show_all(self, username: str) -> list:
        print("Show all activities")
        return self.dao.find_all_by_username(username)

    def show_all_titles(self, username: str) -> list:
        print("Show all titles")
        return [a.name for a in self.show_all(username)]


class EventService:
    def __init__(self):
        self.dao = EventDao()
        self.activity_dao = ActivityDao()

    def create(self, username: str, activity_name: str, event_type: EventType, last: str = None, time=None) -> Event:
        a = self.activity_dao.find_by_username_and_name(username, activity_name)
        if not last:
            last_event = self.find_last(username, activity_name, EventType.STOP)
            last = "first" if not last_event else last_event.id
        e = Event(activity_id=a.id, event_type=event_type, time=time, last=last, username=username)
        self.dao.save(e)
        return e

    def find_last(self, username: str, activity_name: str, event_type: EventType) -> Optional[Event]:
        return self.dao.find_last_event_for_user_activity(username, activity_name, event_type)

    def all_started_activities(self, username) -> list:
        return [self.activity_dao.find_by_id(a_id).name for a_id in self.dao.find_last_started(username)]

    def delete_all(self, username):
        self.dao.delete_all(username)

    def find_last_statistic_events(self, username: str, limit: int):
        self.dao.find_last_events_statistics(username, limit)


class StatisticsService:
    def __init__(self):
        self.event_dao = EventDao()

    def generate(self, username, date_range_str) -> FullStatistics:
        extracted_date_range = time.extract_date_range(date_range_str)
        if extracted_date_range:
            from_d, until_d = extracted_date_range
        else:
            days, weeks, months = time.extract_days_weeks_months(date_range_str)
            until_datetime = datetime.now()
            from_d = time.minus(until_datetime, months=months, weeks=weeks, days=days).date()
            until_d = until_datetime.date()

        assert from_d <= until_d
        statistic: list = self.event_dao.find_statistic_for_date_range(username, from_d, until_d)
        activity_statistic: list = [ActivityStatistics.from_statistic(s) for s in statistic]

        return FullStatistics(activity_statistic=activity_statistic, from_d=from_d, until_d=until_d)
