from aiogram import Dispatcher

from app import state
from app.config import msg, marker
from app.db.entity import EventType
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler, MessageMeta, CallbackMeta
from app.handler.menu import MenuGeneral
from app.service import time_service
from app.service.activity import ActivityService
from app.service.category import CategoryService
from app.service.event import EventService


class TrackCallbackHandler(TelegramCallbackHandler):
    MARKER = marker.TRACK

    def __init__(self, category_service: CategoryService):
        super().__init__()
        self.category_service = category_service

    async def handle_(self, callback: CallbackMeta):
        categories_keyboard = self.category_service.create_all_categories_markup(
            marker=TrackAfterCategoryCallbackHandler.MARKER,
            user_id=callback.user_id,
            back_button_marker=marker.MENU
        )

        await callback.original.message.answer(msg.TRACK_1, reply_markup=categories_keyboard)


class TrackAfterCategoryCallbackHandler(TelegramCallbackHandler):
    MARKER = 'trkac'

    def __init__(self, activity_service: ActivityService):
        super().__init__()
        self.activity_service = activity_service

    async def handle_(self, callback: CallbackMeta):
        category_id = callback.payload[self.MARKER]

        activities_keyboard = self.activity_service.create_all_activities_markup(
            marker=TrackAfterActivityCallbackHandler.MARKER,
            category_id=category_id,
            back_button_marker=marker.TRACK
        )

        await callback.original.message.answer(msg.TRACK_2, reply_markup=activities_keyboard)


class TrackAfterActivityCallbackHandler(TelegramCallbackHandler):
    MARKER = 'trkaa'

    def __init__(self, activity_service: ActivityService):
        super().__init__()
        self.activity_service = activity_service

    async def handle_(self, callback: CallbackMeta):
        activity = self.activity_service.find(callback.payload[self.MARKER])

        await callback.original.message.answer(msg.TRACK_3.format(activity.name))

        await state.TrackWriteTimeRangeState.waiting_for_time_range.set()
        await Dispatcher.get_current().current_state().update_data(activity_name=activity.id)


class TrackAfterTimeAnswerHandler(TelegramMessageHandler, MenuGeneral):
    def __init__(self, activity_service: ActivityService, event_service: EventService):
        super().__init__()
        self.activity_service = activity_service
        self.event_service = event_service

    async def handle_(self, message: MessageMeta, *args):
        activity_id = (await Dispatcher.get_current().current_state().get_data())['activity_name']
        activity = self.activity_service.find(activity_id)

        hours, minutes = time_service.extract_hours_and_minutes(message.text)

        end_time = message.time
        start_time = time_service.minus(end_time, hours=hours, minutes=minutes)

        e_start = self.event_service.create(
            user_id=message.user_id,
            activity_id=activity_id,
            event_type=EventType.START,
            time=start_time)

        self.event_service.create(
            user_id=message.user_id,
            activity_id=activity_id,
            event_type=EventType.STOP,
            time=end_time,
            last=e_start.id)

        await message.original.answer(msg.FINISHED_TRACKING.format(activity.name, hours, minutes))
        await self._show_menu(message.original)
