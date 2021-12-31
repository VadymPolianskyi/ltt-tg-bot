from datetime import datetime
from typing import Optional

import app.util.time as time_service
from app.db import ActivityDao, Activity, EventDao, EventType, Event
from app.statistics import FullStatistics, ActivityStatistics


class ActivityService:
    def __init__(self):
        self.dao = ActivityDao()
        self.event_dao = EventDao()

    def create(self, username: str, activity_name: str) -> Activity:
        print(f"Create activity({activity_name}) for user({username})")
        a = Activity(username=username, name=activity_name)
        self.dao.save(a)
        return a

    def delete(self, username: str, activity_name: str):
        print(f"Delete all  activity({activity_name}) events for user({username})")
        a = self.dao.find_by_username_and_name(username, activity_name)
        self.event_dao.delete_all(username, a.id)
        self.dao.delete(username, a.name)

    def show_all(self, username: str) -> list:
        print(f"Show all activities for user({username})")
        return self.dao.find_all_by_username(username)

    def show_all_titles(self, username: str) -> list:
        print(f"Show all titles for user({username})")
        return [a.name for a in self.show_all(username)]

    def all_started_activity_titles(self, username) -> list:
        print(f"Find last started activities for user({username})")
        started_activities = self.dao.find_last_started(username)
        print(f'Found {len(started_activities)} started activities for user({username})')
        return [a.name for a in started_activities]


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
        print(f'Created {e}')
        return e

    def find_last(self, username: str, activity_name: str, event_type: EventType) -> Optional[Event]:
        return self.dao.find_last_event_for_activity(username, activity_name, event_type)

    def find_last_events_pair(self, username: str, activity_name: str) -> tuple:
        print(f'Find last events pair for activity({activity_name}) of user({username})')
        stop_event = self.dao.find_last_event_for_activity(username, activity_name, EventType.STOP)
        start_event = self.dao.find_by_id(stop_event.last)

        last_event_statistics = ActivityStatistics.from_events(start_event, stop_event, activity_name)
        print(f"Find last completed event for user({username}) - {last_event_statistics.to_str()}")
        return stop_event, start_event, last_event_statistics

    def delete(self, *event_ids):
        self.dao.delete(*event_ids)

    def delete_all(self, username):
        self.dao.delete_all(username)


class StatisticsService:
    def __init__(self):
        self.event_dao = EventDao()

    def generate(self, username, date_range_str) -> FullStatistics:
        extracted_date_range = time_service.extract_date_range(date_range_str)
        if extracted_date_range:
            from_d, until_d = extracted_date_range
        else:
            days, weeks, months = time_service.extract_days_weeks_months(date_range_str)
            until_datetime = datetime.now()
            from_d = time_service.minus(until_datetime, months=months, weeks=weeks, days=days).date()
            until_d = until_datetime.date()

        assert from_d <= until_d
        statistic: list = self.event_dao.find_events_statistics_for_date_range(username, from_d, until_d)
        activity_statistic: list = [ActivityStatistics.from_statistic(s) for s in statistic]

        return FullStatistics(activity_statistic=activity_statistic, from_d=from_d, until_d=until_d)

    def last_events_statistics(self, username: str, limit: str) -> str:
        num_limit = int(limit) if limit.isnumeric() else 20
        print(f"Find last {limit} events for user({username})")

        last_events_statistics = self.event_dao.find_last_events_statistics(username, num_limit)
        statistics = [ActivityStatistics.from_statistic(es) for es in last_events_statistics]
        printed_activities_statistic: str = '\n'.join([s.to_str(with_counter=False) for s in statistics])

        return printed_activities_statistic
