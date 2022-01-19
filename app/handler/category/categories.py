from telebot import TeleBot

from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta
from app.service.category import CategoryService


class CategoriesHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, categories: CategoryService):
        print('Creating CategoriesHandler...')
        super().__init__(bot)
        self.categories = categories

    def handle_(self, message: MessageMeta, *args):
        all_categories_titles = self.categories.show_all_titles(message.user_id)
        str_list = f"\n{msg.CATEGORY_SIGN} " + f"\n{msg.CATEGORY_SIGN} ".join(
            all_categories_titles) if all_categories_titles else "\n Nothing yet..."
        self.bot.send_message(message.user_id, msg.ALL_CATEGORIES.format(str_list))
