from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta
from app.service.category import CategoryService


class CategoriesHandler(TelegramMessageHandler):
    def __init__(self, categories: CategoryService):
        super().__init__()
        self.categories = categories

    async def handle_(self, message: MessageMeta, *args):
        all_categories_titles = self.categories.show_all_names(message.user_id)
        str_list = f"\n{msg.CATEGORY_SIGN} " + f"\n{msg.CATEGORY_SIGN} ".join(
            all_categories_titles) if all_categories_titles else "\n Nothing yet..."

        await message.original.answer(msg.ALL_CATEGORIES.format(str_list))
