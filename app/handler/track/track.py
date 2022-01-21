from aiogram import Dispatcher

from app import state
from app.config import msg
from app.db.entity import EventType
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler, MessageMeta, CallbackMeta
from app.service import time_service
from app.service.activity import ActivityService
from app.service.event import EventService


class TrackHandler(TelegramMessageHandler):
    def __init__(self, activities: ActivityService):
        super().__init__()
        self.activities = activities

    async def handle_(self, message: MessageMeta, *args):
        activities_keyboard = self.activities.all_activities_keyboard(
            message.user_id,
            TrackAfterChoiseCallbackHandler.MARKER
        )

        await message.original.answer(msg.TRACK_1, reply_markup=activities_keyboard)


class TrackAfterChoiseCallbackHandler(TelegramCallbackHandler):
    MARKER = 'track'

    def __init__(self):
        super().__init__()

    async def handle_(self, callback: CallbackMeta):
        activity_name = callback.payload[self.MARKER]

        await callback.original.message.answer(msg.TRACK_2.format(activity_name))

        await state.TrackWriteTimeRangeState.waiting_for_time_range.set()
        await Dispatcher.get_current().current_state().update_data(activity_name=activity_name)


class TrackAfterTimeAnswerHandler(TelegramMessageHandler):
    def __init__(self, events: EventService):
        super().__init__()
        self.events = events

    async def handle_(self, message: MessageMeta, *args):
        activity_name = (await Dispatcher.get_current().current_state().get_data())['activity_name']

        hours, minutes = time_service.extract_hours_and_minutes(message.text)

        end_time = message.time
        start_time = time_service.minus(end_time, hours=hours, minutes=minutes)

        e_start = self.events.create(
            user_id=message.user_id,
            activity_name=activity_name,
            event_type=EventType.START,
            time=start_time)

        self.events.create(
            user_id=message.user_id,
            activity_name=activity_name,
            event_type=EventType.STOP,
            time=end_time,
            last=e_start.id)

        await message.original.answer(msg.FINISHED_TRACKING.format(activity_name, hours, minutes))
