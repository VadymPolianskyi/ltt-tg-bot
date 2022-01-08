from datetime import datetime
from typing import Optional

import app.util.time as time_service
from app.db import ActivityDao, Activity, EventDao, EventType, Event, StatisticsSelector
from app.statistics import FullStatistics, ActivityStatistics


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

    def all_started_activity_titles(self, user_id: int) -> list:
        print(f"Find last started activities for user({str(user_id)})")
        started_activities = self.dao.find_last_started(user_id)
        print(f'Found {len(started_activities)} started activities for user({str(user_id)})')
        return [a.name for a in started_activities]


class EventService:
    def __init__(self):
        self.dao = EventDao()
        self.activity_dao = ActivityDao()

    def create(self, user_id: int, activity_name: str, event_type: EventType, last: str = None, time=None) -> Event:
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


class StatisticsService:
    def __init__(self):
        self.event_dao = EventDao()
        self.activity_dao = ActivityDao()

    def generate(self, user_id: int, date_range_str) -> FullStatistics:
        print(f'Generate statistic for user({user_id}) for {date_range_str}')
        extracted_date_range = time_service.extract_date_range(date_range_str)
        if extracted_date_range:
            from_d, until_d = extracted_date_range
        else:
            days, weeks, months = time_service.extract_days_weeks_months(date_range_str)
            until_datetime = datetime.now()
            from_d = time_service.minus(until_datetime, months=months, weeks=weeks, days=days).date()
            until_d = until_datetime.date()

        assert from_d <= until_d
        statistic: list = StatisticsSelector(user_id) \
            .from_date(from_d) \
            .to_date(until_d) \
            .order_from_newest() \
            .select()
        activity_statistic: list = [ActivityStatistics.from_statistic(s) for s in statistic]

        return FullStatistics(activity_statistic=activity_statistic, from_d=from_d, until_d=until_d)

    def statistics_with_event_id(self, user_id: int, activity_name: str, after_event_id: str = None,
                                 limit: int = 20) -> list:

        activity_id = self.activity_dao.find_by_user_id_and_name(user_id, activity_name).id

        to_date = self.event_dao.find(after_event_id).time.date if after_event_id else datetime.now().date()

        events_statistics: list = StatisticsSelector(user_id) \
            .activity_id(activity_id) \
            .to_date(to_date) \
            .limit(limit) \
            .order_from_newest() \
            .select()

        statistics_with_id = list()
        for es in events_statistics:
            element = (es.stop_event_id, ActivityStatistics.from_statistic(es))
            statistics_with_id.append(element)

        return statistics_with_id

    def last_events_statistics(self, user_id: int, limit: int = 20) -> list:
        print(f"Find last {limit} events for user({str(user_id)})")

        last_events_statistics = StatisticsSelector(user_id) \
            .limit(limit) \
            .order_from_newest() \
            .select()

        statistics = [ActivityStatistics.from_statistic(es) for es in last_events_statistics]

        return statistics
