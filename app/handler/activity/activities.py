from telebot import TeleBot

from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta
from app.service.activity import ActivityService


class ActivitiesHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService):
        print('Creating ActivitiesHandler...')
        super().__init__(bot)
        self.activities = activities

    def handle_(self, message: MessageMeta, *args):
        all_activity_titles = self.activities.show_all_titles(message.user_id)
        str_list = "\n- " + "\n- ".join(all_activity_titles) if all_activity_titles else "\n Nothing yet..."
        self.bot.send_message(message.user_id, msg.ALL_ACTIVITIES.format(str_list))
