from aiogram.types import Message

from app.config import msg, marker
from app.db.entity import Category
from app.handler.general import TelegramCallbackHandler, CallbackMeta
from app.service import markup
from app.service.activity import ActivityService
from app.service.category import CategoryService


class GeneralCategoryHandler:
    def __init__(self, category_service: CategoryService):
        self.category_service = category_service

    async def _show_categories_menu(self, original_message: Message, user_id: int = None):
        if not user_id:
            user_id = original_message.from_user.id
        categories_markup = self.category_service.categories_markup(user_id)
        await original_message.answer(msg.ALL_CATEGORIES, reply_markup=categories_markup)

    async def _show_category_menu(self, original_message: Message, category: Category):
        category_markup = self.category_service.category_markup(category.id)
        await original_message.answer(msg.CATEGORY.format(category.name), reply_markup=category_markup)

    async def _show_category_settings_menu(self, original_message: Message, category: Category):
        category_settings_menu_keyboard = markup.create_inline_markup_([
            (msg.EDIT_NAME_BUTTON, marker.EDIT_CATEGORY_NAME, category.id),
            (msg.DELETE_BUTTON, marker.DELETE_CATEGORY, category.id),
            (msg.BACK_BUTTON, marker.CATEGORY, category.id)
        ])

        await original_message.answer(text=msg.CATEGORY.format(category.name),
                                      reply_markup=category_settings_menu_keyboard)


class CategoriesCallbackHandler(TelegramCallbackHandler, GeneralCategoryHandler):
    MARKER = marker.CATEGORIES

    def __init__(self, category_service: CategoryService, activity_service: ActivityService):
        TelegramCallbackHandler.__init__(self)
        GeneralCategoryHandler.__init__(self, category_service)
        self.activity_service = activity_service

    async def handle_(self, callback: CallbackMeta):
        # migration
        default_category = self.category_service.get_or_create_default(callback.user_id)
        self.activity_service.migrate(callback.user_id, default_category.id)
        # migration

        await self._show_categories_menu(callback.original.message, callback.user_id)


class CategoryCallbackHandler(TelegramCallbackHandler, GeneralCategoryHandler):
    MARKER = marker.CATEGORY

    def __init__(self, category_service: CategoryService):
        TelegramCallbackHandler.__init__(self)
        GeneralCategoryHandler.__init__(self, category_service)

    async def handle_(self, callback: CallbackMeta):
        category = self.category_service.find(callback.payload[self.MARKER])
        await self._show_category_menu(callback.original.message, category)
