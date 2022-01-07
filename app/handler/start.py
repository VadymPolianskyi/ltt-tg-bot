from telebot import TeleBot
from telebot.types import Message

from app.config import msg
from app.handler.general import TelegramMessageHandler


class StartHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot):
        print('Creating StartHandler...')
        super().__init__(bot)

    def handle_(self, message: Message, *args):
        self.bot.send_message(message.chat.id, msg.START)
