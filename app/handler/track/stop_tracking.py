import time

from app.config import msg, marker
from app.handler.general import TelegramCallbackHandler, CallbackMeta
from app.handler.menu import MenuGeneral
from app.service import markup
from app.service.activity import ActivityService
from app.service.event import EventService


class StopTrackingCallbackHandler(TelegramCallbackHandler, MenuGeneral):
    MARKER = marker.STOP_TRACKING

    def __init__(self, activity_service: ActivityService, event_service: EventService):
        super().__init__()
        self.activity_service = activity_service
        self.event_service = event_service

    async def handle_(self, callback: CallbackMeta):
        started_activities = self.activity_service.all_started_activities(callback.user_id)

        if len(started_activities) == 1:
            callback.payload = {StopTrackingAfterVoteCallbackHandler.MARKER: started_activities[0].id}
            await StopTrackingAfterVoteCallbackHandler(self.activity_service, self.event_service).handle_(callback)
        elif len(started_activities) > 1:
            buttons = [(a.name, StopTrackingAfterVoteCallbackHandler.MARKER, a.id) for a in started_activities]
            buttons.append((msg.BACK_BUTTON, marker.MENU, '_'))
            started_activities_keyboard = markup.create_inline_markup_(buttons)
            await callback.original.message.answer(msg.STOP_TRACKING_ACTIVITY, reply_markup=started_activities_keyboard)
        else:
            await callback.original.message.answer(msg.STOP_TRACKING_NOTHING)
            await self._show_menu(callback.original.message)


class StopTrackingAfterVoteCallbackHandler(TelegramCallbackHandler, MenuGeneral):
    MARKER = 'stpa'

    def __init__(self, activity_service: ActivityService, event_service: EventService):
        super().__init__()
        self.activity_service = activity_service
        self.event_service = event_service

    async def handle_(self, callback: CallbackMeta):
        activity = self.activity_service.find(callback.payload[self.MARKER])

        hours, minutes = self.event_service.finish_and_calculate_time(callback.user_id, activity.id, callback.time)
        await callback.original.message.answer(msg.STOP_TRACKING_DONE.format(activity.name, hours, minutes))
        time.sleep(1)
        await self._show_menu(callback.original.message)
