from aiogram.types import Message

from app.config import msg, marker
from app.handler.general import TelegramMessageHandler, MessageMeta, TelegramCallbackHandler, CallbackMeta
from app.service import markup
from app.service.activity import ActivityService


class MenuGeneral:

    def __init__(self, activity_service: ActivityService):
        self.activity_service = activity_service

    async def _show_menu(self, original_message: Message, user_id: int = None):
        if not user_id:
            user_id = original_message.from_user.id

        category_settings_menu_keyboard = markup.create_inline_markup_([
            (msg.CATEGORIES_BUTTON, marker.CATEGORIES, '_'),
            (msg.STATISTICS_BUTTON, marker.STATISTICS, '_'),
            (msg.START_TRACKING_BUTTON, marker.START_TRACKING, '_'),
            (msg.STOP_TRACKING_BUTTON, marker.STOP_TRACKING, '_'),
            (msg.TRACK_BUTTON, marker.TRACK, '_'),
            (msg.SETTINGS_BUTTON, marker.TIME_ZONE, '_')
        ])

        all_started_activities = self.activity_service.all_started_activities(user_id)
        started_activities_txt = ""
        if all_started_activities:
            started_activities_txt += "\nCurrently in progress:\n"
            started_activities_board = ["  " + a.name for a in all_started_activities]
            started_activities_txt += '\n'.join(started_activities_board)
            started_activities_txt += '\n'

        await original_message.answer(msg.MENU.format(started_activities_txt),
                                      reply_markup=category_settings_menu_keyboard)


class MenuHandler(TelegramMessageHandler, MenuGeneral):
    def __init__(self, activity_service: ActivityService):
        TelegramMessageHandler.__init__(self)
        MenuGeneral.__init__(self, activity_service)

    async def handle_(self, message: MessageMeta, *args):
        await self._show_menu(message.original)


class MenuCallbackHandler(TelegramCallbackHandler, MenuGeneral):
    MARKER = marker.MENU

    def __init__(self, activity_service: ActivityService):
        TelegramCallbackHandler.__init__(self)
        MenuGeneral.__init__(self, activity_service)

    async def handle_(self, call: CallbackMeta):
        await self._show_menu(call.original.message, call.user_id)
