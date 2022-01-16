from datetime import date
from datetime import datetime

from app.config import msg
from app.db.dao import ActivityDao, EventDao, StatisticsSelector
from app.db.entity import Event
from app.db.entity import EventStatistic
from app.service import time_service
from app.service.time_service import timedelta_to_minutes, count_difference


class ActivityStatistics:
    def __init__(self, activity: str, from_date: datetime, until_date: datetime, spent_minutes: int):
        self.from_date: datetime.date = from_date
        self.until_date: datetime.date = until_date
        self.spent_minutes: int = spent_minutes
        self.activity_name: str = activity
        self.counter = 1

    def join(self, a_s):
        assert a_s.activity_name == self.activity_name

        self.from_date = self.from_date if self.from_date <= a_s.from_date else a_s.from_date
        self.until_date = self.until_date if self.until_date >= a_s.until_date else a_s.until_date
        self.spent_minutes += a_s.spent_minutes
        self.counter += 1

    def to_str(self, with_single_date=False, with_date_range=False, with_counter=True, prefix: str = ''):
        single_date_str = f'({self.from_date})' if with_single_date else ''
        date_range_str = f'({self.from_date} - {self.until_date})' if with_date_range else ''
        counter_str = f'/ {self.counter} time(s)' if with_counter else ''
        return f'{prefix}{self.activity_name} - {self.format_spent_minutes()} {counter_str} {date_range_str} {single_date_str}'

    def format_spent_minutes(self) -> str:
        spent_hours = int(self.spent_minutes / 60)
        spent_minutes = self.spent_minutes - (spent_hours * 60)

        return f'{spent_hours}h {spent_minutes}m'

    @classmethod
    def from_statistic(cls, statistic: EventStatistic):
        return ActivityStatistics(
            from_date=statistic.date,
            until_date=statistic.date,
            spent_minutes=timedelta_to_minutes(statistic.spent),
            activity=statistic.activity_name
        )

    @classmethod
    def from_events(cls, start_event: Event, stop_event: Event, activity_name: str):
        hours, minutes = count_difference(start_event.time, stop_event.time)
        return ActivityStatistics(
            from_date=start_event.time.date(),
            until_date=stop_event.time.date(),
            spent_minutes=minutes + (hours * 60),
            activity=activity_name
        )


class DailyStatistics:
    def __init__(self, activity_statistic: list, date=None):
        for a_s in activity_statistic:
            assert a_s.from_date == a_s.until_date

        self.date: datetime.date = activity_statistic[0].from_date if date is None else date
        self.statistic: list = self.__aggregate_to_daily(activity_statistic)

    def __aggregate_to_daily(self, activity_statistic) -> list:
        grouped_by_activity = dict()

        for stat in activity_statistic:
            if stat.activity_name in grouped_by_activity.keys():
                grouped_by_activity[stat.activity_name].join(stat)
            else:
                aggregated = stat
                grouped_by_activity[stat.activity_name] = aggregated

        return list(grouped_by_activity.values())


class FullStatistics:
    def __init__(self, activity_statistic: list, from_d: date, until_d: date):
        self.__from_d = from_d
        self.__until_d = until_d
        self.__activity_statistic: list = activity_statistic

    def to_str(self):
        printed_activities_statistic: str = '\n'.join([f.to_str() for f in self.fully()])
        date_str = self.__from_d if self.__from_d == self.__until_d else f'{self.__from_d} - {self.__until_d}'
        return msg.STATISTIC_2.format(date_str, printed_activities_statistic)

    def fully(self) -> list:
        grouped_by_activity = dict()

        for stat in self.__activity_statistic:
            if stat.activity_name in grouped_by_activity.keys():
                grouped_by_activity[stat.activity_name].join(stat)
            else:
                aggregated: ActivityStatistics = stat
                grouped_by_activity[stat.activity_name] = aggregated

        return list(grouped_by_activity.values())

    def daily(self) -> list:

        grouped = dict()

        for act_stat in self.__activity_statistic:
            if act_stat.from_date in grouped.keys():
                grouped[act_stat.from_date].append(act_stat)
            else:
                aggregated = [act_stat]
                grouped[act_stat.from_date] = aggregated

        result = [DailyStatistics(activity_statistic=v, date=k) for k, v in grouped.items()]

        return result


class StatisticsService:
    def __init__(self):
        self.event_dao = EventDao()
        self.activity_dao = ActivityDao()
        self.activity_dao = ActivityDao()

    def generate(self, user_id: int, user_time_zone: str, date_range: str) -> FullStatistics:
        print(f'Generate statistic for user({user_id}) for {date_range}')
        extracted_date_range = time_service.extract_date_range(date_range)
        if extracted_date_range:
            from_d, until_d = extracted_date_range
        else:
            days, weeks, months = time_service.extract_days_weeks_months(date_range)
            until_datetime = time_service.now(user_time_zone)
            from_d = time_service.minus(until_datetime, months=months, weeks=weeks, days=days)
            from_d = time_service.plus(from_d, days=1)
            from_d = from_d.date()
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

        if after_event_id:
            after_event = self.event_dao.find(after_event_id)
            to_date = after_event.time
            activity_id = after_event.activity_id
        else:
            to_date = time_service.now()
            activity_id = self.activity_dao.find_by_user_id_and_name(user_id, activity_name).id

        events_statistics: list = StatisticsSelector(user_id) \
            .activity_id(activity_id) \
            .to_time(to_date) \
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
