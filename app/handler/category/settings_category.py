from app.config import marker
from app.handler.category.category import GeneralCategoryHandler
from app.handler.general import TelegramCallbackHandler, CallbackMeta
from app.service.category import CategoryService


class SettingsCategoryCallbackHandler(TelegramCallbackHandler, GeneralCategoryHandler):
    MARKER = marker.CATEGORY_SETTINGS

    def __init__(self, category_service: CategoryService):
        TelegramCallbackHandler.__init__(self)
        GeneralCategoryHandler.__init__(self, category_service)

    async def handle_(self, callback: CallbackMeta):
        category_id = callback.payload[self.MARKER]

        category = self.category_service.find(category_id)
        await self._show_category_settings_menu(callback.original.message, category)
