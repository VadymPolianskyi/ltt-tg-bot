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
            SELECT * FROM `{self.table_name}` WHERE id=%s;
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


class EventDao:
    def __init__(self):
        self.table_name = config.DB_TABLE_EVENT

    def save(self, event: Event):
        with connection.cursor() as cursor:
            sql_query = f"""
            INSERT INTO `{self.table_name}` (`id`, `activity_id`, `type`, `time`, `last`, `username`)
            VALUES (%s, %s, %s, %s, %s, %s);
            """.replace("'", "")
            cursor.execute(sql_query,
                           (event.id, event.activity_id, event.event_type.name, event.time, event.last, event.username))
        connection.commit()

    def find_last_started(self, username):
        with connection.cursor() as cursor:
            sql_query = f"""
            SELECT DISTINCT activity_id FROM {self.table_name}
            WHERE `username`=%s AND `type`=%s 
            AND  id NOT IN (SELECT `last` FROM {self.table_name} WHERE `username`=%s)
            """.replace("'", "")

            cursor.execute(sql_query, (username, EventType.START.name, username))
            return [r['activity_id'] for r in cursor.fetchall()]

    def find_last_event_for_user_activity(self, username: str, activity_name: str, event_type: EventType) -> Optional[
        Event]:
        with connection.cursor() as cursor:
            sql_query = f"""
                SELECT * FROM {self.table_name} as e
                JOIN ltt_activity as a on a.id=e.activity_id
                WHERE a.name=%s AND e.username=%s AND e.type=%s
                ORDER BY e.time DESC
                LIMIT 1
            """.replace("'", "")

            cursor.execute(sql_query, (activity_name, username, event_type.name))
            r = cursor.fetchone()
            return Event(id=r['id'], activity_id=r['activity_id'], event_type=r['type'], time=r['time'],
                         username=r['username']) if r else None

    def find_statistic_for_date_range(self, username: str, from_d: date, to_d: date) -> list:
        with connection.cursor() as cursor:
            sql_query = f"""
            WITH start_ev as 
            ( 
                SELECT * FROM {self.table_name} WHERE type=%s AND username=%s
            ) 
            SELECT DATE(stop_ev.time) as ev_date, TIMEDIFF(stop_ev.time, start_ev.time) AS spent, activity.name as activity 
            FROM {self.table_name} as stop_ev 
            JOIN start_ev on stop_ev.last=start_ev.id 
            JOIN ltt_activity as activity on stop_ev.activity_id=activity.id 
            WHERE stop_ev.type=%s  AND stop_ev.username=%s
            AND (DATE(stop_ev.time) BETWEEN  %s AND %s)
            """.replace("'", "")
            cursor.execute(sql_query, ('START', username, 'STOP', username, from_d, to_d))
            return [EventStatistic(date=r['ev_date'], spent=r['spent'], activity_name=r['activity']) for r in
                    cursor.fetchall()]

    def find_last_events_statistics(self, username: str, limit: int) -> list:
        with connection.cursor() as cursor:
            sql_query = f"""
            WITH start_ev as 
            ( 
                SELECT * FROM {self.table_name} WHERE type=%s AND username=%s
            ) 
            SELECT DATE(stop_ev.time) as ev_date, TIMEDIFF(stop_ev.time, start_ev.time) AS spent, activity.name as activity 
            FROM {self.table_name} as stop_ev 
            JOIN start_ev on stop_ev.last=start_ev.id 
            JOIN ltt_activity as activity on stop_ev.activity_id=activity.id 
            WHERE stop_ev.type=%s  AND stop_ev.username=%s
            ORDER BY stop_ev.time DESC
            LIMIT %s
            """.replace("'", "")
            cursor.execute(sql_query, ('START', username, 'STOP', username, limit))
            return [EventStatistic(date=r['ev_date'], spent=r['spent'], activity_name=r['activity']) for r in
                    cursor.fetchall()]

    def delete_all_by_activity(self, username: str, activity_id: str):
        with connection.cursor() as cursor:
            sql_query = f"""
            DELETE FROM {self.table_name} WHERE username=%s AND activity_id=%s
            """.replace("'", "")
            cursor.execute(sql_query, (username, activity_id))

    def delete_all(self, username):
        with connection.cursor() as cursor:
            sql_query = f"""
            DELETE FROM {self.table_name} WHERE username=%s
            """.replace("'", "")
            cursor.execute(sql_query, username)
