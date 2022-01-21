from aiogram import Dispatcher

from app import state
from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta, TelegramCallbackHandler, CallbackMeta
from app.service import markup, time_service
from app.service.user import UserService


class TimeZoneHandler(TelegramMessageHandler):
    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service = user_service

    async def handle_(self, message: MessageMeta, *args):
        options_keyboard = markup.create_simple_inline_markup(
            ChangeTimeZoneCallbackHandler.MARKER,
            ["Change Time Zone"]
        )

        user_time_zone: str = self.user_service.get_time_zone(message.user_id)
        current_time = time_service.now(tz=user_time_zone).strftime("%H:%M")
        await message.original.answer(msg.TIMEZONE_1.format(user_time_zone, current_time),
                                      reply_markup=options_keyboard)


class ChangeTimeZoneCallbackHandler(TelegramCallbackHandler):
    MARKER = 'tmz'

    def __init__(self):
        super().__init__()

    async def handle_(self, callback: CallbackMeta):
        await callback.original.message.answer(msg.TIMEZONE_2, disable_web_page_preview=True)
        await state.TimeZoneWriteTZNameState.waiting_for_time_zone_name.set()


class ChangeTimeZoneHandler(TelegramMessageHandler):

    def __init__(self, user_service: UserService):
        super().__init__()
        self.user_service = user_service

    async def handle_(self, message: MessageMeta, *args):
        time_zone: str = message.text
        if time_service.is_valid_time_zone(time_zone):
            self.user_service.update_time_zone(message.user_id, time_zone)
            current_time = time_service.now(tz=time_zone).strftime("%H:%M")

            await message.original.answer(msg.TIMEZONE_3.format(time_zone, current_time))
            await Dispatcher.get_current().current_state().finish()
        else:
            await message.original.answer(msg.TIMEZONE_2, disable_web_page_preview=True)
