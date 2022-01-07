from telebot import TeleBot
from telebot.types import Message

from app.config import msg
from app.handler.general import TelegramMessageHandler
from app.service import ActivityService


class ActivitiesHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService):
        print('Creating ActivitiesHandler...')
        super().__init__(bot)
        self.activities = activities

    def handle_(self, message: Message, *args):
        all_activity_titles = self.activities.show_all_titles(message.from_user.id)
        str_list = "\n- " + "\n- ".join(all_activity_titles) if all_activity_titles else "\n Nothing yet..."
        self.bot.send_message(message.chat.id, msg.ALL_ACTIVITIES.format(str_list))
