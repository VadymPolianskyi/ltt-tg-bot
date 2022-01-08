from telebot import TeleBot
from telebot.types import Message

from app.config import msg
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler
from app.service import ActivityService, EventService, StatisticsService
from app.util import markup
from app.util.markup import EMPTY_VOTE_RESULT


class DeleteEventHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService):
        print('Creating DeleteEventHandler...')
        super().__init__(bot)
        self.activities = activities

    def handle_(self, message: Message, *args):
        activities_keyboard = markup.create_simple_inline_markup(
            DeleteEventBeforeEventsVoteCallbackHandler.MARKER,
            self.activities.show_all_titles(message.from_user.id)
        )

        self.bot.send_message(message.chat.id, msg.DELETE_EVENT_1, reply_markup=activities_keyboard)


class DeleteEventBeforeEventsVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'd_e'

    def __init__(self, bot: TeleBot, statistics_service: StatisticsService):
        print('Creating DeleteEventBeforeEventsVoteCallbackHandler...')
        super().__init__(bot)
        self.statistics_service = statistics_service

    def handle_(self, chat_id: int, payload: dict):
        activity_name = payload[DeleteEventBeforeEventsVoteCallbackHandler.MARKER]

        statistics_with_id = self.statistics_service.statistics_with_event_id(user_id=chat_id,
                                                                              activity_name=activity_name,
                                                                              limit=9)

        last_button = ('Next', 'next')

        button_name_value_tuples = list()
        for s_i in statistics_with_id:
            element = (f'{s_i[1].from_date} - {s_i[1].format_spent_minutes()}', s_i[0])
            button_name_value_tuples.append(element)
        button_name_value_tuples.append(last_button)

        vote_keyboard = markup.create_inline_markup(DeleteEventBeforeVoteCallbackHandler.MARKER,
                                                    button_name_value_tuples)
        self.bot.send_message(chat_id=chat_id, text=msg.DELETE_EVENT_2.format(activity_name),
                              reply_markup=vote_keyboard)


class DeleteEventBeforeVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'd_ev'

    def __init__(self, bot: TeleBot):
        print('Creating DeleteEventBeforeVoteCallbackHandler...')
        super().__init__(bot)

    def handle_(self, chat_id: int, payload: dict):
        event_id = payload[self.MARKER]

        vote_keyboard = markup.create_voter_inline_markup(self.MARKER, event_id)
        self.bot.send_message(chat_id=chat_id, text=msg.DELETE_EVENT_3,
                              reply_markup=vote_keyboard)


class DeleteEventAfterVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = DeleteEventBeforeVoteCallbackHandler.MARKER + markup.VOTE_MARK

    def __init__(self, bot: TeleBot, events: EventService):
        print('Creating DeleteEventAfterVoteCallbackHandler...')
        super().__init__(bot)
        self.events = events

    def handle_(self, chat_id: int, payload: dict):
        vote_result: str = payload[self.MARKER]

        if vote_result != EMPTY_VOTE_RESULT:
            event_id = vote_result
            self.events.delete_pair(event_id)
            self.bot.send_message(chat_id, msg.DELETE_EVENT_4_1)
        else:
            self.bot.send_message(chat_id, msg.DELETE_EVENT_5_1)
