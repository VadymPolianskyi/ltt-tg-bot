from aiogram import Dispatcher

from app.config import msg, marker
from app.handler.activity.activity import GeneralActivityHandler
from app.handler.general import TelegramMessageHandler, MessageMeta, TelegramCallbackHandler, CallbackMeta
from app.service.activity import ActivityService
from app.state import CreateActivityState


class AddActivityCallbackHandler(TelegramCallbackHandler):
    MARKER = marker.ADD_ACTIVITY

    def __init__(self):
        super().__init__()

    async def handle_(self, callback: CallbackMeta):
        category_id = callback.payload[self.MARKER]
        await callback.original.message.answer(msg.ADD_ACTIVITY)
        await CreateActivityState.waiting_for_activity_name.set()
        await Dispatcher.get_current().current_state().update_data(category_id=category_id)


class AddActivityPostAnswerHandler(TelegramMessageHandler, GeneralActivityHandler):
    def __init__(self, activity_service: ActivityService, ):
        TelegramMessageHandler.__init__(self)
        GeneralActivityHandler.__init__(self, activity_service)

    async def handle_(self, message: MessageMeta, *args):
        category_id = (await Dispatcher.get_current().current_state().get_data())['category_id']
        activity_name = message.text

        activity = self.activity_service.create(message.user_id, activity_name, category_id)

        await message.original.answer(msg.ADD_ACTIVITY_DONE.format(activity.name))
        await self._show_activity_settings_menu(message.original, activity)
