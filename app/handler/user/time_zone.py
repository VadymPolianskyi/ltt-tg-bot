from telebot import TeleBot

from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta, TelegramCallbackHandler, CallbackMeta
from app.service import markup, time_service
from app.service.user import UserService


class TimeZoneHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, user_service: UserService):
        print('Creating TimeZoneHandler...')
        super().__init__(bot)
        self.user_service = user_service

    def handle_(self, message: MessageMeta, *args):
        options_keyboard = markup.create_simple_inline_markup(
            ChangeTimeZoneCallbackHandler.MARKER,
            ["Change Time Zone"]
        )

        user_time_zone: str = self.user_service.get_time_zone(message.user_id)
        current_time = time_service.now(tz=user_time_zone).strftime("%H:%M")
        self.bot.send_message(chat_id=message.user_id, text=msg.TIMEZONE_1.format(user_time_zone, current_time),
                              reply_markup=options_keyboard)


class ChangeTimeZoneCallbackHandler(TelegramCallbackHandler):
    MARKER = 'tmz'

    def __init__(self, bot: TeleBot, next_handler: TelegramMessageHandler):
        print('Creating ChangeTimeZoneCallbackHandler...')
        super().__init__(bot)
        self.next_handler = next_handler

    def handle_(self, callback: CallbackMeta):
        self.bot.send_message(callback.user_id, msg.TIMEZONE_2, disable_web_page_preview=True)
        self.bot.register_next_step_handler_by_chat_id(callback.user_id, self.next_handler.handle)


class ChangeTimeZoneHandler(TelegramMessageHandler):

    def __init__(self, bot: TeleBot, user_service: UserService):
        print('Creating ChangeTimeZoneHandler...')
        super().__init__(bot)
        self.user_service = user_service

    def handle_(self, message: MessageMeta, *args):
        time_zone: str = message.text
        if time_service.is_valid_time_zone(time_zone):
            self.user_service.update_time_zone(message.user_id, time_zone)
            current_time = time_service.now(tz=time_zone).strftime("%H:%M")

            self.bot.send_message(message.user_id, msg.TIMEZONE_3.format(time_zone, current_time))
        else:
            self.bot.send_message(message.user_id, msg.TIMEZONE_2, disable_web_page_preview=True)
            self.bot.register_next_step_handler_by_chat_id(message.user_id, self.handle)
