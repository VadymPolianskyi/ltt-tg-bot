import json
from datetime import datetime

from telebot import TeleBot
from telebot.types import CallbackQuery
from telebot.types import Message

from app.config import msg
from app.service import time_service
from app.service.user import UserService


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
        self.user_service = UserService()

    def handle(self, message: Message, *args):
        try:
            user_id = message.from_user.id
            text = message.text

            time_zone: str = self.user_service.get_time_zone(user_id)
            msg_time: datetime = time_service.from_timestamp(message.date, time_zone)

            print(f"Message '{text}' in chat({user_id}) at '{msg_time}'. Args: {','.join(args)}")

            self.handle_(MessageMeta(user_id, msg_time, text), *args)
        except Exception as e:
            print(e)
            self.bot.send_message(message.chat.id, msg.ERROR_BASIC)

    def handle_(self, message: MessageMeta, *args):
        """Response to Message"""
        pass


class TelegramCallbackHandler:
    def __init__(self, bot: TeleBot):
        self.bot = bot
        self.user_service = UserService()

    def handle(self, call: CallbackQuery):
        user_id: int = call.from_user.id
        message_id: int = call.message.id
        time_zone: str = self.user_service.get_time_zone(user_id)
        callback_time: datetime = time_service.from_timestamp(call.message.date, time_zone)

        payload: dict = json.loads(call.data)
        print(f"Callback with payload '{payload}' in chat({user_id}) at '{callback_time}'")

        try:
            self.bot.delete_message(chat_id=user_id, message_id=message_id)

            self.handle_(CallbackMeta(user_id=user_id, time=callback_time, payload=payload))
        except Exception as e:
            print(e)
            self.bot.send_message(user_id, msg.ERROR_BASIC)

    def handle_(self, callback: CallbackMeta):
        """Response to Callback Message"""
        pass
