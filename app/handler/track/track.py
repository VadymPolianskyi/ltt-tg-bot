from telebot import TeleBot
from telebot.types import Message

from app.config import msg
from app.db import EventType
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler, MessageMeta, CallbackMeta
from app.service import ActivityService, EventService
from app.util import markup, time


class TrackHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService):
        print('Creating TrackHandler...')
        super().__init__(bot)
        self.activities = activities

    def handle_(self, message: MessageMeta, *args):
        all_user_activity_titles = self.activities.show_all_titles(message.user_id)
        activities_keyboard = markup.create_simple_inline_markup(
            TrackAfterVoteCallbackHandler.MARKER,
            all_user_activity_titles
        )

        self.bot.send_message(message.user_id, msg.TRACK_1, reply_markup=activities_keyboard)


class TrackPostTimeAnswerHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, events: EventService):
        print('Creating TrackPostTimeAnswerHandler...')
        super().__init__(bot)
        self.events = events

    def handle_(self, message: MessageMeta, *args):
        assert args
        activity = args[0]

        hours_and_minutes_str: str = message.text
        hours, minutes = time.extract_hours_and_minutes(hours_and_minutes_str)

        end_time = message.time
        start_time = time.minus(end_time, hours=hours, minutes=minutes)

        e_start = self.events.create(
            user_id=message.user_id,
            activity_name=activity,
            event_type=EventType.START,
            time=start_time)

        self.events.create(
            user_id=message.user_id,
            activity_name=activity,
            event_type=EventType.STOP,
            time=end_time,
            last=e_start.id)

        self.bot.send_message(message.user_id, msg.FINISHED_TRACKING.format(activity, hours, minutes))


class TrackAfterVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'track'

    def __init__(self, bot: TeleBot, track_post_time_answer_handler: TrackPostTimeAnswerHandler):
        print('Creating TrackAfterVoteCallbackHandler...')
        super().__init__(bot)
        self.track_post_time_answer_handler = track_post_time_answer_handler

    def handle_(self, callback: CallbackMeta):
        activity_name = callback.payload[self.MARKER]

        self.bot.send_message(callback.user_id, msg.TRACK_2.format(activity_name))

        self.bot.register_next_step_handler_by_chat_id(
            callback.user_id,
            self.track_post_time_answer_handler.handle,
            activity_name
        )
