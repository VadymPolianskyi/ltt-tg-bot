from datetime import datetime, date
from typing import Optional

import pymysql

from app.config import config
from app.db.entity import Activity, EventType, Event, EventStatistic, User, Category

connection = pymysql.connect(
    host=config.DB_HOST,
    port=config.DB_PORT,
    user=config.DB_USERNAME,
    passwd=config.DB_PASSWORD,
    database=config.DB_NAME,
    cursorclass=pymysql.cursors.DictCursor)


class Dao:
    def _select_one(self, query, parameters):
        with connection.cursor() as cursor:
            sql_query = query.replace("'", "")
            print(f"Execute 'select_one' query: {sql_query}")
            print(f'Parameters: {parameters}')
            cursor.execute(sql_query, parameters)
            print("Successfully selected")
            return cursor.fetchone()

    def _select_list(self, query, parameters) -> list:
        with connection.cursor() as cursor:
            sql_query = query.replace("'", "")
            print(f"Execute 'select_list' query: {sql_query}")
            print(f'Parameters: {parameters}')
            cursor.execute(sql_query, parameters)
            print("Successfully selected")
            return cursor.fetchall()

    def _execute(self, query, parameters):
        with connection.cursor() as cursor:
            sql_query = query.replace("'", "")
            print(f"Execute query: {sql_query}")
            print(f'Parameters: {parameters}')
            cursor.execute(sql_query, parameters)
            print("Successfully executed")
        connection.commit()


class UserDao(Dao):
    def __init__(self):
        self.__table = config.DB_TABLE_USER

    def find(self, user_id: int) -> Optional[User]:
        query = f'SELECT * FROM `{self.__table}` WHERE id=%s;'
        r = self._select_one(query, user_id)
        return User.from_dict(r) if r else None

    def save(self, user: User):
        query = f'INSERT INTO `{self.__table}` (`id`, `username`, `time_zone`) VALUES (%s, %s, %s);'
        self._execute(query, (user.id, user.username, user.time_zone))

    def update_time_zone(self, user_id: int, time_zone: str):
        query = f'UPDATE `{self.__table}` SET time_zone = %s WHERE id=%s;'
        self._execute(query, (time_zone, user_id))


class CategoryDao(Dao):
    def __init__(self):
        self.__category_table_name = config.DB_TABLE_CATEGORY

    def save(self, category: Category):
        query = f'INSERT INTO `{self.__category_table_name}` (`id`, `user_id`, `name`) VALUES (%s, %s, %s);'
        self._execute(query, (category.id, category.user_id, category.name))

    def delete(self, id: str):
        print(f"Delete Category({id})")
        query = f'DELETE FROM `{self.__category_table_name}` WHERE id=%s'
        self._execute(query, id)

    def find_all_by_user_id(self, user_id: int) -> list:
        print(f"Select all categories for User({user_id})")
        query = f'SELECT * FROM `{self.__category_table_name}` WHERE user_id=%s;'
        result = self._select_list(query, user_id)
        return [Category.from_dict(r) for r in result]

    def find(self, id: str) -> Optional[Category]:
        print(f"Find Category({id})")
        query = f'SELECT * FROM `{self.__category_table_name}` WHERE id=%s;'
        r = self._select_one(query, id)
        return Category.from_dict(r) if r else None


class ActivityDao(Dao):
    def __init__(self):
        self.__activity_table_name = config.DB_TABLE_ACTIVITY
        self.__event_table_name = config.DB_TABLE_EVENT

    def save(self, activity: Activity):
        query = f'INSERT INTO `{self.__activity_table_name}` (`id`, `user_id`, `name`) VALUES (%s, %s, %s);'
        self._execute(query, (activity.id, activity.user_id, activity.name))

    def delete(self, user_id: int, name):
        query = f'DELETE FROM `{self.__activity_table_name}` WHERE user_id=%s AND name=%s'
        self._execute(query, (user_id, name))

    def find_all_by_user_id(self, user_id: int) -> list:
        print(f"Select all activities for user_id '{str(user_id)}")
        query = f'SELECT * FROM `{self.__activity_table_name}` WHERE user_id=%s;'
        result = self._select_list(query, user_id)
        return [Activity.from_dict(r) for r in result]

    def find_all_by_categoty_id(self, category_id: str) -> list:
        print(f"Select all activities for category_id '{str(category_id)}")
        query = f'SELECT * FROM `{self.__activity_table_name}` WHERE category_id=%s;'
        result = self._select_list(query, category_id)
        return [Activity.from_dict(r) for r in result]

    def find(self, activity_id: str) -> Optional[Activity]:
        query = f'SELECT * FROM `{self.__activity_table_name}` WHERE id=%s;'
        r = self._select_one(query, activity_id)
        return Activity.from_dict(r) if r else None

    # todo: replace this on querying by id
    def find_by_user_id_and_name(self, user_id: int, activity_name: str):
        query = f'SELECT * FROM `{self.__activity_table_name}` WHERE user_id=%s AND name=%s;'
        r = self._select_one(query, (user_id, activity_name))
        return Activity.from_dict(r) if r else None

    def find_last_started(self, user_id: int) -> list:
        query = f"""
                SELECT DISTINCT a.id, a.name, a.user_id, a.created FROM `{self.__event_table_name}` as e
                JOIN `{self.__activity_table_name}` as a on e.activity_id=a.id
                WHERE e.user_id=%s AND e.type=%s 
                AND  e.id NOT IN (SELECT `last` FROM `{self.__event_table_name}` WHERE `user_id`=%s)
                """
        result = self._select_list(query, (user_id, EventType.START.name, user_id))
        return [Activity.from_dict(r) for r in result]


class EventDao(Dao):
    def __init__(self):
        super().__init__()
        self.__activity_table_name = config.DB_TABLE_ACTIVITY
        self.__event_table_name = config.DB_TABLE_EVENT

    def save(self, event: Event):
        query = f'INSERT INTO `{self.__event_table_name}` (`id`, `activity_id`, `type`, `time`, `last`, `user_id`) ' + \
                'VALUES (%s, %s, %s, %s, %s, %s);'
        self._execute(query,
                      (event.id, event.activity_id, event.event_type.name, event.time, event.last, event.user_id))

    def find(self, event_id: str) -> Optional[Event]:
        query = f'SELECT * FROM `{self.__event_table_name}` WHERE `id`=%s;'
        r = self._select_one(query, event_id)

        return Event.from_dict(r) if r else None

    def find_last_event_for_activity(self, user_id: int, activity_name: str, event_type: EventType) -> Optional[Event]:
        query = f"""
        SELECT * FROM `{self.__event_table_name}` as e
                JOIN `{self.__activity_table_name}` as a ON e.activity_id=a.id
                WHERE a.name=%s AND e.user_id=%s AND e.type=%s
                AND e.id NOT IN (SELECT `last` FROM `{self.__event_table_name}` WHERE `user_id`=%s)
                ORDER BY e.time DESC
                LIMIT 1
        """
        r = self._select_one(query, (activity_name, user_id, event_type.name, user_id))
        return Event.from_dict(r) if r else None

    def delete_all_for_activity(self, activity_id: str):
        query = f'DELETE FROM {self.__event_table_name} WHERE activity_id=%s'
        self._execute(query, activity_id)

    def delete(self, *event_ids):
        event_ids_conndition = " or ".join(["id=%s" for _ in event_ids]) if event_ids else ''
        query = f'DELETE FROM {self.__event_table_name} WHERE {event_ids_conndition}'
        self._execute(query, event_ids)


class StatisticsSelector(Dao):
    def __init__(self, user_id: int):
        super().__init__()
        self.__activity_table_name = config.DB_TABLE_ACTIVITY
        self.__event_table_name = config.DB_TABLE_EVENT

        self.__query_parameters = tuple()
        self.__dynamic_conditions = str()
        self.__user_id = user_id
        self.__activity_id = None
        self.__from_d = None
        self.__to_d = None
        self.__to_t = None

        self.__order: str = ''
        self.__limit: str = ''
        self.__activity_conndition: str = ''
        self.__from_date_conndition: str = ''
        self.__to_date_conndition: str = ''
        self.__to_time_conndition: str = ''

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

    def to_time(self, to_t: datetime):
        self.__to_time_conndition = 'AND stop_ev.time <= %s'
        self.__to_t = to_t.strftime('%Y-%m-%d %H:%M:%S')
        return self

    def limit(self, limit: int):
        self.__limit: str = f'LIMIT {limit}'
        return self

    def order_from_newest(self):
        self.__order = 'ORDER BY stop_ev.time DESC'
        return self

    def __prepare_conditions(self):
        all_conditions = [
            self.__from_date_conndition,
            self.__to_date_conndition,
            self.__activity_conndition,
            self.__to_time_conndition
        ]

        filtered = [c for c in all_conditions if c != '']

        self.__dynamic_conditions = ' '.join(filtered)

    def __prepare_query_params(self):
        all_query_parameters = [
            EventType.START.name,
            self.__user_id,
            EventType.STOP.name,
            self.__user_id,
            self.__from_d,
            self.__to_d,
            self.__activity_id,
            self.__to_t
        ]
        filtered_qp = [p for p in all_query_parameters if p is not None]

        self.__query_parameters = tuple(filtered_qp)

    def __build_sql_query(self) -> str:
        return f"""WITH start_ev as 
                    ( 
                        SELECT * FROM `{self.__event_table_name}` WHERE type=%s AND user_id=%s
                    ) 
                    SELECT DATE(stop_ev.time) as ev_date, TIMEDIFF(stop_ev.time, start_ev.time) AS spent, a.name as activity, stop_ev.id AS event_id
                    FROM {self.__event_table_name} as stop_ev 
                    JOIN start_ev on stop_ev.last=start_ev.id 
                    JOIN {self.__activity_table_name} as a on stop_ev.activity_id=a.id 
                    WHERE stop_ev.type=%s  AND stop_ev.user_id=%s {self.__dynamic_conditions}
                    {self.__order} {self.__limit}
                """

    def select(self) -> list:
        self.__prepare_conditions()
        self.__prepare_query_params()

        result = self._select_list(self.__build_sql_query(), self.__query_parameters)
        return [EventStatistic.from_dict(r) for r in result]
