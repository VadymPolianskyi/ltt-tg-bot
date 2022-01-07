import uuid
from datetime import datetime, timedelta, date
from enum import Enum
from typing import Optional

import pymysql

from app.config import config

connection = pymysql.connect(
    host=config.DB_HOST,
    port=config.DB_PORT,
    user=config.DB_USERNAME,
    passwd=config.DB_PASSWORD,
    database=config.DB_NAME,
    cursorclass=pymysql.cursors.DictCursor)


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


class Dao:
    def __init__(self):
        self._activity_table_name = config.DB_TABLE_ACTIVITY
        self._event_table_name = config.DB_TABLE_EVENT


class ActivityDao(Dao):
    def __init__(self):
        super().__init__()

    def save(self, activity: Activity):
        with connection.cursor() as cursor:
            sql_query = f"""
            INSERT INTO `{self._activity_table_name}` (`id`, `user_id`, `name`) VALUES (%s, %s, %s);
            """.replace("'", "")

            cursor.execute(sql_query, (activity.id, activity.user_id, activity.name))
        connection.commit()

    def delete(self, user_id: int, name):
        with connection.cursor() as cursor:
            sql_query = f"DELETE FROM `{self._activity_table_name}` WHERE user_id=%s AND name=%s".replace("'", "")
            cursor.execute(sql_query, (user_id, name))
        connection.commit()

    def find_all_by_user_id(self, user_id: int):
        print(f"Select all activities for user_id '{str(user_id)}")
        with connection.cursor() as cursor:
            sql_query = f"SELECT * FROM `{self._activity_table_name}` WHERE user_id=%s;".replace("'", "")

            cursor.execute(sql_query, user_id)
            print("Successfully selected")
            return [Activity(name=r['name'], user_id=r['user_id'], created=r['created'], id=r['id']) for r in
                    cursor.fetchall()]

    def find(self, activity_id: str):
        with connection.cursor() as cursor:
            sql_query = f"""
            SELECT * FROM `{self._activity_table_name}` WHERE id=%s ;
            """.replace("'", "")

            cursor.execute(sql_query, activity_id)
            r = cursor.fetchone()
            return Activity(name=r['name'], user_id=r['user_id'], created=r['created'], id=r['id'])

    def find_by_user_id_and_name(self, user_id: int, activity_name: str):
        with connection.cursor() as cursor:
            sql_query = f"""
            SELECT * FROM `{self._activity_table_name}` WHERE user_id=%s AND name=%s;
            """.replace("'", "")

            cursor.execute(sql_query, (user_id, activity_name))
            r = cursor.fetchone()
            return Activity(name=r['name'], user_id=r['user_id'], created=r['created'], id=r['id'])

    def find_last_started(self, user_id: int) -> list:
        with connection.cursor() as cursor:
            sql_query = f"""
            SELECT DISTINCT a.id, a.name, a.created FROM `{self._event_table_name}` as e
            JOIN `{self._activity_table_name}` as a on e.activity_id=a.id
            WHERE e.user_id=%s AND e.type=%s 
            AND  e.id NOT IN (SELECT `last` FROM `{self._event_table_name}` WHERE `user_id`=%s)
            """.replace("'", "")

            cursor.execute(sql_query, (user_id, EventType.START.name, user_id))
            return [Activity(name=r['name'], user_id=user_id, created=r['created'], id=r['id']) for r in
                    cursor.fetchall()]


class EventDao(Dao):
    def __init__(self):
        super().__init__()

    def save(self, event: Event):
        with connection.cursor() as cursor:
            sql_query = f"""
            INSERT INTO `{self._event_table_name}` (`id`, `activity_id`, `type`, `time`, `last`, `user_id`)
            VALUES (%s, %s, %s, %s, %s, %s);
            """.replace("'", "")
            cursor.execute(sql_query,
                           (event.id, event.activity_id, event.event_type.name, event.time, event.last, event.user_id))
        connection.commit()

    def find(self, event_id: str):
        with connection.cursor() as cursor:
            sql_query = f"""
            SELECT * FROM `{self._event_table_name}` WHERE `id`=%s;            
            """.replace("'", "")

            cursor.execute(sql_query, event_id)
            r = cursor.fetchone()
            return Event(id=r['id'], activity_id=r['activity_id'], event_type=r['type'], time=r['time'],
                         user_id=r['user_id'])

    def find_last_event_for_activity(self, user_id: int, activity_name: str, event_type: EventType) -> Optional[Event]:
        with connection.cursor() as cursor:
            sql_query = f"""
                SELECT * FROM `{self._event_table_name}` as e
                JOIN `{self._activity_table_name}` as a ON e.activity_id=a.id
                WHERE a.name=%s AND e.user_id=%s AND e.type=%s
                ORDER BY e.time DESC
                LIMIT 1
            """.replace("'", "")

            cursor.execute(sql_query, (activity_name, user_id, event_type.name))
            r = cursor.fetchone()
            return Event(id=r['id'], activity_id=r['activity_id'], event_type=r['type'], time=r['time'],
                         user_id=r['user_id'], last=r['last']) if r else None

    def delete(self, user_id: int, activity_id: str = None, *event_ids):
        with connection.cursor() as cursor:
            activity_condition: str = " AND activity_id=%s" if activity_id else ''
            event_ids_conndition = " AND " + " or ".join(["id=%s" for _ in event_ids]) if event_ids else ''

            all_query_parameters = [user_id, activity_id] + list(event_ids)
            query_parameters = tuple([p for p in all_query_parameters if p is not None])

            sql_query = f"""
            DELETE FROM {self._event_table_name} WHERE user_id=%s {activity_condition} {event_ids_conndition}
            """.replace("'", "")
            cursor.execute(sql_query, query_parameters)


class StatisticsSelector(Dao):
    def __init__(self, user_id: int):
        super().__init__()
        self.__query_parameters = tuple()
        self.__user_id = user_id
        self.__activity_id = None
        self.__from_d = None
        self.__to_d = None

        self.__order: str = ''
        self.__limit: str = ''
        self.__activity_conndition: str = ''
        self.__from_date_conndition: str = ''
        self.__to_date_conndition: str = ''

    def activity_id(self, activity_id: str):
        self.__activity_conndition = 'AND stop_ev.activity_id=%s'
        self.__activity_id = activity_id
        return self

    def from_date(self, from_d: date):
        self.__from_date_conndition = 'AND DATE(stop_ev.time) >= %s'
        self.__from_d = from_d
        return self

    def to_date(self, to_d: date):
        self.__to_date_conndition = 'AND DATE(stop_ev.time) <= %s'
        self.__to_d = to_d
        return self

    def limit(self, limit: int):
        self.__limit: str = f'LIMIT {limit}'
        return self

    def order_from_newest(self):
        self.__order = 'ORDER BY stop_ev.time DESC'
        return self

    def __prepare_query_params(self):
        all_query_parameters = [
            EventType.START.name,
            self.__user_id,
            EventType.STOP.name,
            self.__user_id,
            self.__from_d,
            self.__to_d,
            self.__activity_id
        ]
        filtered_qp = [p for p in all_query_parameters if p is not None]

        self.__query_parameters = tuple(filtered_qp)

    def select(self) -> list:
        self.__prepare_query_params()
        with connection.cursor() as cursor:
            sql_query = f"""
            WITH start_ev as 
            ( 
                SELECT * FROM `{self._event_table_name}` WHERE type=%s AND user_id=%s
            ) 
            SELECT DATE(stop_ev.time) as ev_date, TIMEDIFF(stop_ev.time, start_ev.time) AS spent, a.name as activity, stop_ev.id AS event_id
            FROM {self._event_table_name} as stop_ev 
            JOIN start_ev on stop_ev.last=start_ev.id 
            JOIN {self._activity_table_name} as a on stop_ev.activity_id=a.id 
            WHERE stop_ev.type=%s  AND stop_ev.user_id=%s {self.__from_date_conndition} {self.__to_date_conndition} {self.__activity_conndition}
            {self.__order} {self.__limit}
            """.replace("'", "").strip()
            cursor.execute(sql_query, self.__query_parameters)
            return [
                EventStatistic(
                    date=r['ev_date'],
                    spent=r['spent'],
                    activity_name=r['activity'],
                    stop_event_id=r['event_id']
                ) for r in cursor.fetchall()
            ]
