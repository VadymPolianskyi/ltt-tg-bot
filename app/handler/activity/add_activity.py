from telebot import TeleBot
from telebot.types import Message

from app.config import msg
from app.handler.general import TelegramMessageHandler
from app.service import ActivityService


class AddActivityPostAnswerHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService):
        super().__init__(bot)
        self.activities = activities

    def handle_(self, message: Message, *args):
        activity_name = message.text
        activity = self.activities.create(message.from_user.id, activity_name)

        self.bot.send_message(message.chat.id, msg.ADD_ACTIVITY_2.format(activity.name))


class AddActivityHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService,
                 add_activity_post_answer_handler: AddActivityPostAnswerHandler):
        print('Creating AddActivityHandler...')
        super().__init__(bot)
        self.add_activity_post_answer_handler = add_activity_post_answer_handler
        self.activities = activities

    def handle_(self, message: Message, *args):
        self.bot.send_message(message.from_user.id, msg.ADD_ACTIVITY_1)
        self.bot.register_next_step_handler_by_chat_id(message.chat.id, self.add_activity_post_answer_handler.handle)
