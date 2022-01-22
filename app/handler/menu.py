from aiogram.types import Message

from app.config import msg, marker
from app.handler.general import TelegramMessageHandler, MessageMeta, TelegramCallbackHandler, CallbackMeta
from app.service import markup


class MenuGeneral:

    async def _show_menu(self, original_message: Message):
        category_settings_menu_keyboard = markup.create_inline_markup_([
            (msg.CATEGORIES_BUTTON, marker.CATEGORIES, '_'),
            (msg.STATISTICS_BUTTON, marker.STATISTICS, '_'),
            (msg.START_TRACKING_BUTTON, marker.START_TRACKING, '_'),
            (msg.STOP_TRACKING_BUTTON, marker.STOP_TRACKING, '_'),
            (msg.TRACK_BUTTON, marker.TRACK, '_'),
            (msg.SETTINGS_BUTTON, marker.TIME_ZONE, '_')
        ])
        await original_message.answer(msg.MENU, reply_markup=category_settings_menu_keyboard)


class MenuHandler(TelegramMessageHandler, MenuGeneral):
    def __init__(self):
        TelegramMessageHandler.__init__(self)

    async def handle_(self, message: MessageMeta, *args):
        await self._show_menu(message.original)


class MenuCallbackHandler(TelegramCallbackHandler, MenuGeneral):
    MARKER = marker.MENU

    def __init__(self):
        TelegramCallbackHandler.__init__(self)

    async def handle_(self, call: CallbackMeta):
        await self._show_menu(call.original.message)
