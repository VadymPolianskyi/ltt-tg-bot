from aiogram import Dispatcher

from app.config import msg, marker
from app.handler.category.category import GeneralCategoryHandler
from app.handler.general import TelegramCallbackHandler, TelegramMessageHandler, MessageMeta, CallbackMeta
from app.service.category import CategoryService
from app.state import EditCategoryState


class EditCategoryNameCallbackHandler(TelegramCallbackHandler):
    MARKER = marker.EDIT_CATEGORY_NAME

    def __init__(self, category_service: CategoryService):
        super().__init__()
        self.category_service = category_service

    async def handle_(self, callback: CallbackMeta):
        category_id = callback.payload[self.MARKER]
        category = self.category_service.find(category_id)

        await callback.original.message.answer(msg.EDIT_CATEGORY_NAME.format(category.name))
        await EditCategoryState.waiting_for_category_name.set()
        await Dispatcher.get_current().current_state().update_data(category_id=category_id)


class EditCategoryNameAfterAnswerHandler(TelegramMessageHandler, GeneralCategoryHandler):
    def __init__(self, category_service: CategoryService):
        TelegramMessageHandler.__init__(self)
        GeneralCategoryHandler.__init__(self, category_service)

    async def handle_(self, message: MessageMeta, *args):
        category_id = (await Dispatcher.get_current().current_state().get_data())['category_id']

        category = self.category_service.find(category_id)
        new_name = message.text
        old_name = category.name

        category.name = new_name
        self.category_service.update(category)

        await message.original.answer(msg.EDIT_CATEGORY_NAME_DONE.format(old_name, new_name))
        await self._show_category_menu(message.original, category)
