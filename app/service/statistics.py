from datetime import date
from datetime import datetime

from app.config import msg
from app.db.dao import ActivityDao, EventDao, StatisticsSelector
from app.db.entity import EventStatistic
from app.service import time_service
from app.service.time_service import timedelta_to_minutes


class Statistics:
    def __init__(self, category: str, activity: str, from_date: datetime, until_date: datetime, spent_minutes: int):
        self.from_date: datetime.date = from_date
        self.until_date: datetime.date = until_date
        self.spent_minutes: int = spent_minutes
        self.category_name: str = category
        self.activity_name: str = activity
        self.counter = 1

    def join(self, a_s):
        assert a_s.category_name == self.category_name and a_s.activity_name == self.activity_name

        self.from_date = self.from_date if self.from_date <= a_s.from_date else a_s.from_date
        self.until_date = self.until_date if self.until_date >= a_s.until_date else a_s.until_date
        self.spent_minutes += a_s.spent_minutes
        self.counter += 1

    def to_str(self, with_single_date=False, with_date_range=False, with_counter=True, prefix: str = ''):
        single_date_str = f'({self.from_date})' if with_single_date else ''
        date_range_str = f'({self.from_date} - {self.until_date})' if with_date_range else ''
        counter_str = f'/ {self.counter} time(s)' if with_counter else ''
        return f'{prefix}{self.activity_name} - {time_service.minutes_to_str_time(self.spent_minutes)} {counter_str} {date_range_str} {single_date_str}'

    @classmethod
    def from_statistic(cls, statistic: EventStatistic):
        return Statistics(
            from_date=statistic.date,
            until_date=statistic.date,
            spent_minutes=timedelta_to_minutes(statistic.spent),
            category=statistic.category_name,
            activity=statistic.activity_name
        )


class CategoryStatistics:
    def __init__(self, category_name: str, statistics: list):
        self.category_name = category_name
        self.statistics = statistics

    def to_str(self):
        printed_statistics: str = '   ' + '\n   '.join([f.to_str() for f in self.statistics])
        return msg.STATISTICS_CATEGORY_RESULT.format(self.category_name, printed_statistics)


class FullStatistics:
    def __init__(self, statistics: list, from_d: date, until_d: date):
        self.__from_d = from_d
        self.__until_d = until_d
        self.statistics: list = self.__aggregate_to_categories(statistics)

    def __aggregate_to_categories(self, statistics: list) -> list:
        grouped_by_category = dict()

        for s in statistics:
            if s.category_name in grouped_by_category.keys():
                grouped_by_category[s.category_name].append(s)
            else:
                grouped_by_category[s.category_name] = [s]

        return [CategoryStatistics(k, self.__aggregate_by_activity(v)) for k, v in grouped_by_category.items()]

    def __aggregate_by_activity(self, statistics: list) -> list:
        grouped_by_activity = dict()

        for s in statistics:
            if s.activity_name in grouped_by_activity.keys():
                grouped_by_activity[s.activity_name].join(s)
            else:
                grouped_by_activity[s.activity_name] = s

        return list(grouped_by_activity.values())

    def to_str(self):
        printed_statistics: str = '\n'.join([s.to_str() for s in self.statistics])
        date_str = self.__from_d if self.__from_d == self.__until_d else f'{self.__from_d} - {self.__until_d}'
        return msg.STATISTIC_RESULT.format(date_str, printed_statistics)


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
        activity_statistic: list = [Statistics.from_statistic(s) for s in statistic]

        return FullStatistics(statistics=activity_statistic, from_d=from_d, until_d=until_d)

    def statistics_with_event_id(self, user_id: int, activity_id: str, after_event_id: str = None,
                                 limit: int = 20) -> list:

        to_date = self.event_dao.find(after_event_id).time if after_event_id else time_service.now()

        events_statistics: list = StatisticsSelector(user_id) \
            .activity_id(activity_id) \
            .to_time(to_date) \
            .limit(limit) \
            .order_from_newest() \
            .select()

        return [(es.stop_event_id, Statistics.from_statistic(es)) for es in events_statistics]

    def last_events_statistics(self, user_id: int, activity_id: str, limit: int = 20) -> list:
        print(f"Find last {limit} events for user({str(user_id)})")

        last_events_statistics = StatisticsSelector(user_id) \
            .activity_id(activity_id) \
            .limit(limit) \
            .order_from_newest() \
            .select()

        statistics = [Statistics.from_statistic(es) for es in last_events_statistics]

        return statistics
