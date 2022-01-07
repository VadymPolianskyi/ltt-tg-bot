from telebot import TeleBot
from telebot.types import Message

from app.config import msg
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler
from app.service import ActivityService
from app.util import markup


class DeleteActivityHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService):
        print('Creating DeleteActivityHandler...')
        super().__init__(bot)
        self.activities = activities

    def handle_(self, message: Message, *args):
        all_user_activity_titles = self.activities.show_all_titles(message.from_user.id)
        activities_keyboard = markup.create_inline_markup(DeleteActivityBeforeVoteCallbackHandler.MARKER,
                                                          all_user_activity_titles)

        self.bot.send_message(message.chat.id, msg.DELETE_ACTIVITY_1, reply_markup=activities_keyboard)


class DeleteActivityBeforeVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'delete'

    def __init__(self, bot: TeleBot):
        print('Creating DeleteActivityBeforeVoteCallbackHandler...')
        super().__init__(bot)

    def handle_(self, chat_id: int, payload: dict):
        activity_name = payload[self.MARKER]

        vote_keyboard = markup.create_activity_voter_markup(self.MARKER, activity_name)
        self.bot.send_message(chat_id=chat_id, text=msg.DELETE_ACTIVITY_2.format(activity_name),
                              reply_markup=vote_keyboard)


class DeleteActivityAfterVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = DeleteActivityBeforeVoteCallbackHandler.MARKER + '_vote'

    def __init__(self, bot: TeleBot, activities: ActivityService):
        print('Creating DeleteActivityAfterVoteCallbackHandler...')
        super().__init__(bot)
        self.activities = activities

    def handle_(self, chat_id: int, payload: dict):
        vote = payload['delete_vote']
        activity_name = payload['payload']
        if vote == "Yes":
            self.activities.delete(chat_id, activity_name)
            self.bot.send_message(chat_id, msg.DELETE_ACTIVITY_3_1.format(activity_name))
        else:
            self.bot.send_message(chat_id, msg.DELETE_ACTIVITY_4_1.format(activity_name))
