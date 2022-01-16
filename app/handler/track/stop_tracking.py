from telebot import TeleBot

from app.config import msg
from app.db.entity import EventType
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler, MessageMeta, CallbackMeta
from app.service import time, markup
from app.service.activity import ActivityService
from app.service.event import EventService


class StopTrackingAfterVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'stop_tracking'

    def __init__(self, bot: TeleBot, events: EventService):
        print('Creating StartTrackingAfterVoteCallbackHandler...')
        super().__init__(bot)
        self.events = events

    def handle_(self, callback: CallbackMeta):
        activity = callback.payload[StopTrackingAfterVoteCallbackHandler.MARKER]

        e_start = self.events.find_last(callback.user_id, activity, EventType.START)
        e_stop = self.events.create(
            user_id=callback.user_id,
            activity_name=activity,
            event_type=EventType.STOP,
            time=callback.time,
            last=e_start.id
        )

        hours, minutes = time.count_difference(e_start.time, e_stop.time)

        self.bot.send_message(callback.user_id, msg.STOP_TRACKING_2_2.format(activity, hours, minutes))


class StopTrackingHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService,
                 stop_tracking_after_vote_callback_handler: StopTrackingAfterVoteCallbackHandler):
        print('Creating StopTrackingHandler...')
        super().__init__(bot)
        self.activities = activities
        self.stop_tracking_after_vote_callback_handler = stop_tracking_after_vote_callback_handler

    def handle_(self, message: MessageMeta, *args):
        started_activities = self.activities.all_started_activity_titles(message.user_id)

        if len(started_activities) == 1:
            payload = {StopTrackingAfterVoteCallbackHandler.MARKER: started_activities[0]}
            self.stop_tracking_after_vote_callback_handler.handle_(CallbackMeta(message.user_id, message.time, payload))

        elif len(started_activities) > 1:
            activities_keyboard = markup.create_simple_inline_markup(StopTrackingAfterVoteCallbackHandler.MARKER,
                                                                     started_activities)
            self.bot.send_message(message.user_id, msg.STOP_TRACKING_2_1, reply_markup=activities_keyboard)

        else:
            self.bot.send_message(message.user_id, msg.STOP_TRACKING_3_1)
