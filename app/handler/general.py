import json
from datetime import datetime

from telebot import TeleBot
from telebot.types import CallbackQuery
from telebot.types import Message

from app.config import msg


class MessageMeta:
    def __init__(self, user_id: int, time: datetime, text: str):
        self.user_id = user_id
        self.time = time
        self.text = text


class CallbackMeta:
    def __init__(self, user_id: int, time: datetime, payload: dict):
        self.user_id = user_id
        self.time = time
        self.payload = payload


class TelegramMessageHandler:

    def __init__(self, bot: TeleBot):
        self.bot = bot

    def handle(self, message: Message, *args):
        try:

            chat_id = message.chat.id
            time = datetime.fromtimestamp(message.date)
            text = message.text

            print(f"Message '{text}' in chat({chat_id}) at '{time}'. Args: {','.join(args)}")

            args = args + (message.from_user.username,)  # temp

            self.handle_(MessageMeta(chat_id, time, text), *args)
        except Exception as e:
            print(e)
            self.bot.send_message(message.chat.id, msg.ERROR_BASIC)

    def handle_(self, message: MessageMeta, *args):
        """Response to Message"""
        pass


class TelegramCallbackHandler:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def handle(self, call: CallbackQuery):
        chat_id: int = call.from_user.id
        message_id: int = call.message.id
        time = datetime.fromtimestamp(call.message.date)

        payload: dict = json.loads(call.data)
        print(f"Callback with payload '{payload}' in chat({chat_id}) at '{time}'")

        try:
            self.bot.delete_message(chat_id=chat_id, message_id=message_id)

            self.handle_(CallbackMeta(user_id=chat_id, time=time, payload=payload))
        except Exception as e:
            print(e)
            self.bot.send_message(chat_id, msg.ERROR_BASIC)

    def handle_(self, callback: CallbackMeta):
        """Response to Callback Message"""
        pass
