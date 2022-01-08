from telebot import TeleBot

from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta


class StartHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot):
        print('Creating StartHandler...')
        super().__init__(bot)

    def handle_(self, message: MessageMeta, *args):
        self.bot.send_message(message.user_id, msg.START)
