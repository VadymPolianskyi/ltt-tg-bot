from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta
from app.service.category import CategoryService


class AddCategoryHandler(TelegramMessageHandler):
    def __init__(self):
        super().__init__()

    async def handle_(self, message: MessageMeta, *args):
        await message.original.answer(msg.ADD_CATEGORY_1)


class AddCategoryPostAnswerHandler(TelegramMessageHandler):
    def __init__(self, categories: CategoryService):
        super().__init__()
        self.categories = categories

    async def handle_(self, message: MessageMeta, *args):
        category_name = message.text
        category = self.categories.create(message.user_id, category_name)

        await message.original.answer(msg.ADD_CATEGORY_2.format(category.name))
