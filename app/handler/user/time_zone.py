from aiogram import Dispatcher
from aiogram.types import Message

from app import state
from app.config import msg, marker
from app.handler.general import TelegramMessageHandler, MessageMeta, TelegramCallbackHandler, CallbackMeta
from app.service import markup, time_service
from app.service.user import UserService


class GeneralTimeZoneHandler:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def _show_current_time_zone_menu(self, original_message: Message, user_id: int):
        tz_menu = markup.create_inline_markup_([
            (msg.CHANGE_TIME_ZONE_BUTTON, TimeZoneWriteCallbackHandler.MARKER, '_'),
            (msg.BACK_BUTTON, marker.MENU, '_')
        ])

        user_time_zone: str = self.user_service.get_time_zone(user_id)
        current_time = time_service.now(tz=user_time_zone).strftime("%H:%M")
        await original_message.answer(msg.TIMEZONE_CURRENT.format(user_time_zone, current_time), reply_markup=tz_menu)


class TimeZoneCallbackHandler(TelegramCallbackHandler, GeneralTimeZoneHandler):
    MARKER = marker.TIME_ZONE

    def __init__(self, user_service: UserService):
        TelegramCallbackHandler.__init__(self)
        GeneralTimeZoneHandler.__init__(self, user_service)

    async def handle_(self, callback: CallbackMeta):
        await self._show_current_time_zone_menu(callback.original.message, callback.user_id)


class TimeZoneWriteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'tmzch'

    def __init__(self):
        super().__init__()

    async def handle_(self, callback: CallbackMeta):
        await callback.original.message.answer(msg.TIMEZONE_EDIT, disable_web_page_preview=True)
        await state.TimeZoneWriteTZNameState.waiting_for_time_zone_name.set()


class ChangeTimeZoneHandler(TelegramMessageHandler, GeneralTimeZoneHandler):

    def __init__(self, user_service: UserService):
        TelegramCallbackHandler.__init__(self)
        GeneralTimeZoneHandler.__init__(self, user_service)

    async def handle_(self, message: MessageMeta, *args):
        time_zone: str = message.text
        if time_service.is_valid_time_zone(time_zone):
            self.user_service.update_time_zone(message.user_id, time_zone)

            await Dispatcher.get_current().current_state().finish()
            await self._show_current_time_zone_menu(message.original, message.user_id)
        else:
            await message.original.answer(msg.TIMEZONE_EDIT, disable_web_page_preview=True)
