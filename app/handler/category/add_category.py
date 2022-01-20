from telebot import TeleBot

from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta
from app.service.category import CategoryService


class AddCategoryHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, next_handler: TelegramMessageHandler):
        print('Creating AddCategoryHandler...')
        super().__init__(bot)
        self.next_handler = next_handler

    def handle_(self, message: MessageMeta, *args):
        self.bot.send_message(message.user_id, msg.ADD_CATEGORY_1)
        self.bot.register_next_step_handler_by_chat_id(message.user_id, self.next_handler.handle)


class AddCategoryPostAnswerHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, categories: CategoryService):
        print('Creating AddCategoryPostAnswerHandler...')
        super().__init__(bot)
        self.categories = categories

    def handle_(self, message: MessageMeta, *args):
        category_name = message.text
        category = self.categories.create(message.user_id, category_name)

        self.bot.send_message(message.user_id, msg.ADD_CATEGORY_2.format(category.name))
