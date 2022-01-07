from telebot import TeleBot
from telebot.types import Message

from app.config import msg
from app.db import EventType
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler
from app.service import ActivityService, EventService
from app.util import markup, time


class StopTrackingAfterVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'stop_tracking'

    def __init__(self, bot: TeleBot, events: EventService):
        print('Creating StartTrackingAfterVoteCallbackHandler...')
        super().__init__(bot)
        self.events = events

    def handle_(self, chat_id: int, payload: dict):
        activity = payload[StopTrackingAfterVoteCallbackHandler.MARKER]

        e_start = self.events.find_last(chat_id, activity, EventType.START)
        e_stop = self.events.create(user_id=chat_id, activity_name=activity, event_type=EventType.STOP, last=e_start.id)

        hours, minutes = time.count_difference(e_start.time, e_stop.time)

        self.bot.send_message(chat_id, msg.STOP_TRACKING_2_2.format(activity, hours, minutes))


class StopTrackingHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService,
                 stop_tracking_after_vote_callback_handler: StopTrackingAfterVoteCallbackHandler):
        print('Creating StopTrackingHandler...')
        super().__init__(bot)
        self.activities = activities
        self.stop_tracking_after_vote_callback_handler = stop_tracking_after_vote_callback_handler

    def handle_(self, message: Message, *args):
        started_activities = self.activities.all_started_activity_titles(message.from_user.id)
        if len(started_activities) == 1:
            self.stop_tracking_after_vote_callback_handler.handle_(
                chat_id=message.chat.id, payload={StopTrackingAfterVoteCallbackHandler.MARKER: started_activities[0]})

        elif len(started_activities) > 1:
            activities_keyboard = markup.create_inline_markup(StopTrackingAfterVoteCallbackHandler.MARKER,
                                                              started_activities)
            self.bot.send_message(message.chat.id, msg.STOP_TRACKING_2_1, reply_markup=activities_keyboard)

        else:
            self.bot.send_message(message.chat.id, msg.STOP_TRACKING_3_1)