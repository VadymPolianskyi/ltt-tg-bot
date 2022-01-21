from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateCategoryState(StatesGroup):
    waiting_for_category_name = State()


class CreateActivityState(StatesGroup):
    waiting_for_activity_name = State()


class StatisticWriteTimeRangeState(StatesGroup):
    waiting_for_time_range = State()


class TrackWriteTimeRangeState(StatesGroup):
    waiting_for_time_range = State()


class TimeZoneWriteTZNameState(StatesGroup):
    waiting_for_time_zone_name = State()


class LastEventsWriteCountState(StatesGroup):
    waiting_for_count = State()
