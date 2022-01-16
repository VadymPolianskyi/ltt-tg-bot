from telebot import TeleBot

from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta
from app.service.activity import ActivityService


class AddActivityHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService,
                 next_handler: TelegramMessageHandler):
        print('Creating AddActivityHandler...')
        super().__init__(bot)
        self.next_handler = next_handler
        self.activities = activities

    def handle_(self, message: MessageMeta, *args):
        self.bot.send_message(message.user_id, msg.ADD_ACTIVITY_1)
        self.bot.register_next_step_handler_by_chat_id(message.user_id, self.next_handler.handle)


class AddActivityPostAnswerHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService):
        super().__init__(bot)
        self.activities = activities

    def handle_(self, message: MessageMeta, *args):
        activity_name = message.text
        activity = self.activities.create(message.user_id, activity_name)

        self.bot.send_message(message.user_id, msg.ADD_ACTIVITY_2.format(activity.name))
