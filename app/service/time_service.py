import re
from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def now(tz: str = None) -> datetime:
    return datetime.now(tz=ZoneInfo(tz)) if tz else datetime.now()


def timedelta_to_minutes(spent: timedelta) -> int:
    spent_seconds = spent.seconds
    spent_minutes = int(spent_seconds / 60)
    return spent_minutes


def count_difference(start_time: datetime, stop_time: datetime):
    days_difference = stop_time.day - stop_time.day
    hours_difference = stop_time.hour - start_time.hour
    minutes_difference = stop_time.minute - start_time.minute
    if minutes_difference < 0:
        hours_difference = hours_difference - 1
        minutes_difference = minutes_difference + 60

    hours = int(hours_difference + (days_difference * 24))
    minutes = int(minutes_difference)
    return hours, minutes


def extract_date_range(date_range: str) -> Optional[tuple]:
    date_range = date_range.strip().replace(' ', "")

    m = re.search(r'(\d+\.\d+\.\d+)-(\d+\.\d+\.\d+)', date_range)

    if not m:
        return None
    else:
        from_date_str = m.group(1) + " 00:00:00"
        from_date = datetime.strptime(from_date_str, '%d.%m.%Y %H:%M:%S')
        until_date_str = m.group(2) + " 00:00:00"
        until_date = datetime.strptime(until_date_str, '%d.%m.%Y %H:%M:%S')
        return from_date.date(), until_date.date()


def extract_days_weeks_months(days_weeks_months_str: str):
    days_weeks_months_str = days_weeks_months_str.strip().replace(' ', "")
    m = re.search('((.+?)d)?((.+?)?w)?((.+?)?m)?', days_weeks_months_str, re.IGNORECASE)

    if not m:
        print("ERROR")

    days = int(m.group(2)) if m.group(1) else 0
    weeks = m.group(4) if m.group(3) else 0
    months = m.group(6) if m.group(5) else 0

    return int(days), int(weeks), int(months)


def extract_hours_and_minutes(hours_and_minutes_str: str):
    hours_and_minutes_str = hours_and_minutes_str.strip().replace(' ', "")
    m = re.search('((.+?)h)?((.+?)?m)?', hours_and_minutes_str, re.IGNORECASE)

    if not m:
        print("ERROR")

    hours = m.group(2) if m.group(1) else 0
    minutes = m.group(4) if m.group(3) else 0

    return int(hours), int(minutes)


def minus(dt: datetime, months: int = 0, weeks: int = 0, days: int = 0, hours: int = 0, minutes: int = 0) -> datetime:
    if months > 0:
        days += months * 30

    return dt - timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)


def plus(dt: datetime, months: int = 0, weeks: int = 0, days: int = 0, hours: int = 0, minutes: int = 0) -> datetime:
    if months > 0:
        days += months * 30

    return dt + timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)


def is_valid_time_zone(time_zone: str) -> bool:
    try:
        now(tz=time_zone)
        return True
    except ZoneInfoNotFoundError as e:
        return False


def to_tz(t: datetime, tz: str):
    return t.astimezone(tz=ZoneInfo(tz))


def from_timestamp(t: int, tz: str):
    return datetime.fromtimestamp(t, ZoneInfo(tz))
