from app.config import msg
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler, MessageMeta, CallbackMeta
from app.service import markup
from app.service.activity import ActivityService
from app.service.category import CategoryService
from app.service.markup import EMPTY_VOTE_RESULT


class DeleteCategoryHandler(TelegramMessageHandler):
    def __init__(self, categories: CategoryService):
        super().__init__()
        self.categories = categories

    async def handle_(self, message: MessageMeta, *args):
        categories_touples = [(c.name, c.id) for c in self.categories.all(message.user_id)]

        categories_keyboard = markup.create_inline_markup(
            DeleteCategoryBeforeVoteCallbackHandler.MARKER,
            categories_touples
        )

        await message.original.answer(text=msg.DELETE_CATEGORY_1, reply_markup=categories_keyboard)


class DeleteCategoryBeforeVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'd_c'

    def __init__(self, categories: CategoryService, activities: ActivityService):
        super().__init__()
        self.categories = categories
        self.activities = activities

    async def handle_(self, callback: CallbackMeta):
        category_id = callback.payload[self.MARKER]

        category = self.categories.find(category_id)

        is_empty = len(self.activities.find_all(category_id)) == 0

        if is_empty:
            vote_keyboard = markup.create_voter_inline_markup(self.MARKER, category_id)

            await callback.original.message.answer(
                text=msg.DELETE_CATEGORY_2.format(category.name),
                reply_markup=vote_keyboard
            )
        else:
            await callback.original.answer(text=msg.DELETE_CATEGORY_3.format(category.name))


class DeleteCategoryAfterVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = DeleteCategoryBeforeVoteCallbackHandler.MARKER + markup.VOTE_MARK

    def __init__(self, categories: CategoryService):
        super().__init__()
        self.categories = categories

    async def handle_(self, callback: CallbackMeta):
        vote_result = callback.payload[self.MARKER]

        if vote_result != EMPTY_VOTE_RESULT:
            category_id = vote_result
            category = self.categories.find(category_id)
            self.categories.delete(category_id)
            await callback.original.message.answer(msg.DELETE_CATEGORY_4.format(category.name))
        else:
            await callback.original.message.answer(msg.DELETE_CATEGORY_5)
