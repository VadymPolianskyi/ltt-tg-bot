from app.config import msg
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler, MessageMeta, CallbackMeta
from app.service import markup
from app.service.activity import ActivityService
from app.service.event import EventService


class StopTrackingHandler(TelegramMessageHandler):
    def __init__(self, activities: ActivityService, events: EventService):
        super().__init__()
        self.activities = activities
        self.events = events

    async def handle_(self, message: MessageMeta, *args):
        started_activities = self.activities.all_started_activity_titles(message.user_id)

        if len(started_activities) == 1:
            activity = started_activities[0]
            hours, minutes = self.events.finish_and_calculate_time(message.user_id, activity, message.time)
            await message.original.answer(msg.STOP_TRACKING_2_2.format(activity, hours, minutes))

        elif len(started_activities) > 1:
            started_activities_keyboard = markup.create_simple_inline_markup(
                StopTrackingAfterVoteCallbackHandler.MARKER,
                started_activities
            )
            await message.original.answer(msg.STOP_TRACKING_2_1, reply_markup=started_activities_keyboard)
        else:
            await message.original.answer(msg.STOP_TRACKING_3_1)


class StopTrackingAfterVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 's_t'

    def __init__(self, events: EventService):
        super().__init__()
        self.events = events

    async def handle_(self, callback: CallbackMeta):
        activity = callback.payload[StopTrackingAfterVoteCallbackHandler.MARKER]

        hours, minutes = self.events.finish_and_calculate_time(callback.user_id, activity, callback.time)
        await callback.original.message.answer(msg.STOP_TRACKING_2_2.format(activity, hours, minutes))
