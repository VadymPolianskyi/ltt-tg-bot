from telebot import TeleBot

from app.config import msg
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler, MessageMeta, CallbackMeta
from app.service.activity import ActivityService
from app.service.category import CategoryService
from app.service import markup
from app.service.markup import EMPTY_VOTE_RESULT


class DeleteCategoryHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, categories: CategoryService):
        print('Creating DeleteCategoryHandler...')
        super().__init__(bot)
        self.categories = categories

    def handle_(self, message: MessageMeta, *args):
        categories_touples = [(c.name, c.id) for c in self.categories.all(message.user_id)]

        categories_keyboard = markup.create_inline_markup(
            DeleteCategoryBeforeVoteCallbackHandler.MARKER,
            categories_touples
        )

        self.bot.send_message(message.user_id, msg.DELETE_CATEGORY_1, reply_markup=categories_keyboard)


class DeleteCategoryBeforeVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'd_c'

    def __init__(self, bot: TeleBot, categories: CategoryService, activities: ActivityService):
        print('Creating DeleteCategoryBeforeVoteCallbackHandler...')
        super().__init__(bot)
        self.categories = categories
        self.activities = activities

    def handle_(self, callback: CallbackMeta):
        category_id = callback.payload[self.MARKER]

        category = self.categories.find(category_id)

        is_empty = len(self.activities.find_all(category_id)) == 0

        if is_empty:
            vote_keyboard = markup.create_voter_inline_markup(self.MARKER, category_id)

            self.bot.send_message(
                chat_id=callback.user_id,
                text=msg.DELETE_CATEGORY_2.format(category.name),
                reply_markup=vote_keyboard
            )
        else:
            self.bot.send_message(chat_id=callback.user_id, text=msg.DELETE_CATEGORY_3.format(category.name))


class DeleteCategoryAfterVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = DeleteCategoryBeforeVoteCallbackHandler.MARKER + markup.VOTE_MARK

    def __init__(self, bot: TeleBot, categories: CategoryService):
        print('Creating DeleteCategoryAfterVoteCallbackHandler...')
        super().__init__(bot)
        self.categories = categories

    def handle_(self, callback: CallbackMeta):
        vote_result = callback.payload[self.MARKER]

        if vote_result != EMPTY_VOTE_RESULT:
            category_id = vote_result
            category = self.categories.find(category_id)
            self.categories.delete(category_id)
            self.bot.send_message(callback.user_id, msg.DELETE_CATEGORY_4.format(category.name))
        else:
            self.bot.send_message(callback.user_id, msg.DELETE_CATEGORY_5)
