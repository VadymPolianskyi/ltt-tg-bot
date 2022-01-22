from app.config import msg, marker
from app.handler.category.category import GeneralCategoryHandler
from app.handler.general import TelegramMessageHandler, MessageMeta, TelegramCallbackHandler, CallbackMeta
from app.service.category import CategoryService
from app.state import CreateCategoryState


class AddCategoryCallbackHandler(TelegramCallbackHandler):
    MARKER = marker.ADD_CATEGORY

    def __init__(self):
        super().__init__()

    async def handle_(self, callback: CallbackMeta):
        await callback.original.message.answer(msg.ADD_CATEGORY)
        await CreateCategoryState.waiting_for_category_name.set()


class AddCategoryAfterAnswerHandler(TelegramMessageHandler, GeneralCategoryHandler):
    def __init__(self, category_service: CategoryService):
        TelegramMessageHandler.__init__(self)
        GeneralCategoryHandler.__init__(self, category_service)

    async def handle_(self, message: MessageMeta, *args):
        category_name = message.text
        self.category_service.create(message.user_id, category_name)

        await message.original.answer(msg.ADD_CATEGORY_DONE.format(category_name))
        await self._show_categories_menu(message.original)
