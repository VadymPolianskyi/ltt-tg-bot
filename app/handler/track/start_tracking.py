from telebot import TeleBot

from app.config import msg
from app.db import EventType
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler, MessageMeta, CallbackMeta
from app.service import ActivityService, EventService
from app.util import markup


class StartTrackingHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService):
        print('Creating StartTrackingHandler...')
        super().__init__(bot)
        self.activities = activities

    def handle_(self, message: MessageMeta, *args):
        started_titles = self.activities.all_started_activity_titles(message.user_id)
        all_user_activity_titles = [a for a in self.activities.show_all_titles(message.user_id) if
                                    a not in started_titles]

        activities_keyboard = markup.create_simple_inline_markup(StartTrackingAfterVoteCallbackHandler.MARKER,
                                                                 all_user_activity_titles)

        self.bot.send_message(message.user_id, msg.START_TRACKING_1, reply_markup=activities_keyboard)


class StartTrackingAfterVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'start_tracking'

    def __init__(self, bot: TeleBot, events: EventService):
        print('Creating StartTrackingAfterVoteCallbackHandler...')
        super().__init__(bot)
        self.events = events

    def handle_(self, callback: CallbackMeta):
        activity_name = callback.payload[self.MARKER]

        self.events.create(
            user_id=callback.user_id,
            activity_name=activity_name,
            event_type=EventType.START,
            time=callback.time
        )
        self.bot.send_message(callback.user_id, msg.START_TRACKING_2.format(activity_name))
