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
    def __init__(self, name: str, username: str, created: datetime = None, id: str = None, ):
        self.name = name
        self.username = username
        self.id = uuid.uuid4() if id is None else id
        self.created = created


class EventType(Enum):
    START = 1
    STOP = 2


class Event:
    def __init__(self, activity_id: str, event_type: EventType, username: str, id=None, last: str = None,
                 time: datetime = None):
        self.id = uuid.uuid4() if id is None else id
        self.activity_id = activity_id
        self.event_type = event_type
        self.time = datetime.now() if time is None else time
        self.last = last
        self.username = username


class EventStatistic:
    def __init__(self, date: datetime, spent: timedelta, activity_name: str):
        self.date: datetime = date
        self.spent: timedelta = spent
        self.activity_name: str = activity_name


class ActivityDao:
    def __init__(self):
        self.table_name = config.DB_TABLE_ACTIVITY
        self.event_table_name = config.DB_TABLE_EVENT

    def save(self, activity: Activity):
        with connection.cursor() as cursor:
            sql_query = f"INSERT INTO `{self.table_name}` (`id`, `username`, `name`) VALUES (%s, %s, %s);".replace("'",
                                                                                                                   "")
            cursor.execute(sql_query, (activity.id, activity.username, activity.name))
        connection.commit()

    def delete(self, username, name):
        with connection.cursor() as cursor:
            sql_query = f"DELETE FROM `{self.table_name}` WHERE username=%s AND name=%s".replace("'", "")
            cursor.execute(sql_query, (username, name))
        connection.commit()

    def find_all_by_username(self, username: str):
        print(f"Select all activities for username '{username}")
        with connection.cursor() as cursor:
            sql_query = f"SELECT * FROM `{self.table_name}` WHERE username=%s;".replace("'", "")

            cursor.execute(sql_query, username)
            print("Successfully selected")
            return [Activity(name=r['name'], username=r['username'], created=r['created'], id=r['id']) for r in
                    cursor.fetchall()]

    def find_by_id(self, activity_id: str):
        with connection.cursor() as cursor:
            sql_query = f"""
            SELECT * FROM `{self.table_name}` WHERE id=%s ;
            """.replace("'", "")

            cursor.execute(sql_query, activity_id)
            r = cursor.fetchone()
            return Activity(name=r['name'], username=r['username'], created=r['created'], id=r['id'])

    def find_by_username_and_name(self, username: str, activity_name: str):
        with connection.cursor() as cursor:
            sql_query = f"""
            SELECT * FROM `{self.table_name}` WHERE username=%s AND name=%s;
            """.replace("'", "")

            cursor.execute(sql_query, (username, activity_name))
            r = cursor.fetchone()
            return Activity(name=r['name'], username=r['username'], created=r['created'], id=r['id'])

    def find_last_started(self, username) -> list:
        with connection.cursor() as cursor:
            sql_query = f"""
            SELECT DISTINCT a.id, a.name, a.created FROM `{self.event_table_name}` as e
            JOIN `{self.table_name}` as a on e.activity_id=a.id
            WHERE e.username=%s AND e.type=%s 
            AND  e.id NOT IN (SELECT `last` FROM `{self.event_table_name}` WHERE `username`=%s)
            """.replace("'", "")

            cursor.execute(sql_query, (username, EventType.START.name, username))
            return [Activity(name=r['name'], username=username, created=r['created'], id=r['id']) for r in
                    cursor.fetchall()]


class EventDao:
    def __init__(self):
        self.table_name = config.DB_TABLE_EVENT
        self.activity_table_name = config.DB_TABLE_ACTIVITY

    def save(self, event: Event):
        with connection.cursor() as cursor:
            sql_query = f"""
            INSERT INTO `{self.table_name}` (`id`, `activity_id`, `type`, `time`, `last`, `username`)
            VALUES (%s, %s, %s, %s, %s, %s);
            """.replace("'", "")
            cursor.execute(sql_query,
                           (event.id, event.activity_id, event.event_type.name, event.time, event.last, event.username))
        connection.commit()

    def find_by_id(self, event_id: str):
        with connection.cursor() as cursor:
            sql_query = f"""
            SELECT * FROM `{self.table_name}` WHERE `id`=%s;            
            """.replace("'", "")

            cursor.execute(sql_query, event_id)
            r = cursor.fetchone()
            return Event(id=r['id'], activity_id=r['activity_id'], event_type=r['type'], time=r['time'],
                         username=r['username'])

    def find_last_event_for_activity(self, username: str, activity_name: str, event_type: EventType) -> Optional[Event]:
        with connection.cursor() as cursor:
            sql_query = f"""
                SELECT * FROM `{self.table_name}` as e
                JOIN `{self.activity_table_name}` as a ON e.activity_id=a.id
                WHERE a.name=%s AND e.username=%s AND e.type=%s
                ORDER BY e.time DESC
                LIMIT 1
            """.replace("'", "")

            cursor.execute(sql_query, (activity_name, username, event_type.name))
            r = cursor.fetchone()
            return Event(id=r['id'], activity_id=r['activity_id'], event_type=r['type'], time=r['time'],
                         username=r['username'], last=r['last']) if r else None

    def find_events_statistics_for_date_range(self, username: str, from_d: date, to_d: date) -> list:
        with connection.cursor() as cursor:
            sql_query = f"""
            WITH start_ev as 
            ( 
                SELECT * FROM {self.table_name} WHERE type=%s AND username=%s
            ) 
            SELECT DATE(stop_ev.time) as ev_date, TIMEDIFF(stop_ev.time, start_ev.time) AS spent, activity.name as activity 
            FROM {self.table_name} as stop_ev 
            JOIN start_ev on stop_ev.last=start_ev.id 
            JOIN {self.activity_table_name} as activity on stop_ev.activity_id=activity.id 
            WHERE stop_ev.type=%s  AND stop_ev.username=%s
            AND (DATE(stop_ev.time) BETWEEN  %s AND %s)
            """.replace("'", "")
            cursor.execute(sql_query, (EventType.START.name, username, EventType.STOP.name, username, from_d, to_d))
            return [EventStatistic(date=r['ev_date'], spent=r['spent'], activity_name=r['activity']) for r in
                    cursor.fetchall()]

    def find_last_events_statistics(self, username: str, limit: int) -> list:
        with connection.cursor() as cursor:
            sql_query = f"""
            WITH start_ev as 
            ( 
                SELECT * FROM `{self.table_name}` WHERE type=%s AND username=%s
            ) 
            SELECT DATE(stop_ev.time) as ev_date, TIMEDIFF(stop_ev.time, start_ev.time) AS spent, a.name as activity 
            FROM {self.table_name} as stop_ev 
            JOIN start_ev on stop_ev.last=start_ev.id 
            JOIN {self.activity_table_name} as a on stop_ev.activity_id=a.id 
            WHERE stop_ev.type=%s  AND stop_ev.username=%s
            ORDER BY stop_ev.time DESC
            LIMIT {limit}
            """.replace("'", "")
            cursor.execute(sql_query, (EventType.START.name, username, EventType.STOP.name, username))
            return [EventStatistic(date=r['ev_date'], spent=r['spent'], activity_name=r['activity']) for r in
                    cursor.fetchall()]

    def delete(self, *event_ids):
        with connection.cursor() as cursor:
            dynamic_conndition = " or ".join(["id=%s" for e in event_ids])

            sql_query = f"""
            DELETE FROM {self.table_name} WHERE {dynamic_conndition}
            """.replace("'", "")
            cursor.execute(sql_query, event_ids)

    def delete_all(self, username, activity_id: str = None):
        with connection.cursor() as cursor:
            activity_condition: str = " AND activity_id=%s" if activity_id else ''
            query_parameters = (username, activity_id) if activity_id else username

            sql_query = f"""
            DELETE FROM {self.table_name} WHERE username=%s {activity_condition}
            """.replace("'", "")
            cursor.execute(sql_query, query_parameters)
