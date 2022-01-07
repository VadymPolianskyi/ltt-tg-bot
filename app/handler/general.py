import json

from telebot import TeleBot
from telebot.types import CallbackQuery
from telebot.types import Message

from app.config import msg


class TelegramMessageHandler:

    def __init__(self, bot: TeleBot):
        self.bot = bot

    def handle(self, message: Message, *args):
        try:
            print(f"Message '{message.text}' in chat({message.chat.id}). Args: {','.join(args)}")

            self.handle_(message, *args)
        except Exception as e:
            print(e)
            self.bot.send_message(message.chat.id, msg.ERROR_BASIC)

    def handle_(self, message: Message, *args):
        """Response to Message"""
        pass


class TelegramCallbackHandler:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def handle(self, call: CallbackQuery):
        chat_id: int = call.from_user.id
        message_id: int = call.message.id

        payload: dict = json.loads(call.data)
        print(f"Callback with payload '{payload}' in chat({chat_id})")

        try:
            self.bot.delete_message(chat_id=chat_id, message_id=message_id)
            self.handle_(chat_id, payload)
        except Exception as e:
            print(e)
            self.bot.send_message(chat_id, msg.ERROR_BASIC)

    def handle_(self, chat_id: int, payload: dict):
        """Response to Callback Message"""
        pass
