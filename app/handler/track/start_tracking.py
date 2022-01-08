from telebot import TeleBot
from telebot.types import Message

from app.config import msg
from app.db import EventType
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler
from app.service import ActivityService, EventService
from app.util import markup


class StartTrackingHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService):
        print('Creating StartTrackingHandler...')
        super().__init__(bot)
        self.activities = activities

    def handle_(self, message: Message, *args):
        started_titles = self.activities.all_started_activity_titles(message.from_user.id)
        all_user_activity_titles = [a for a in self.activities.show_all_titles(message.from_user.id) if
                                    a not in started_titles]

        activities_keyboard = markup.create_simple_inline_markup(StartTrackingAfterVoteCallbackHandler.MARKER,
                                                                 all_user_activity_titles)

        self.bot.send_message(message.chat.id, msg.START_TRACKING_1, reply_markup=activities_keyboard)


class StartTrackingAfterVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'start_tracking'

    def __init__(self, bot: TeleBot, events: EventService):
        print('Creating StartTrackingAfterVoteCallbackHandler...')
        super().__init__(bot)
        self.events = events

    def handle_(self, chat_id: int, payload: dict):
        activity_name = payload[self.MARKER]

        self.events.create(chat_id, activity_name, EventType.START)
        self.bot.send_message(chat_id, msg.START_TRACKING_2.format(activity_name))
