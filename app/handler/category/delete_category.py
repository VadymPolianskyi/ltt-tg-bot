from app.config import msg, marker
from app.handler.category.category import GeneralCategoryHandler
from app.handler.general import TelegramCallbackHandler, CallbackMeta
from app.service import markup
from app.service.activity import ActivityService
from app.service.category import CategoryService
from app.service.markup import EMPTY_VOTE_RESULT


class DeleteCategoryCallbackHandler(TelegramCallbackHandler):
    MARKER = marker.DELETE_CATEGORY

    def __init__(self, categories: CategoryService, activities: ActivityService):
        super().__init__()
        self.categories = categories
        self.activities = activities

    async def handle_(self, callback: CallbackMeta):
        category_id = callback.payload[self.MARKER]

        category = self.categories.find(category_id)

        is_empty = len(self.activities.all(category_id)) == 0

        if is_empty:
            vote_keyboard = markup.create_voter_inline_markup(self.MARKER, category_id)

            await callback.original.message.answer(
                text=msg.DELETE_CATEGORY.format(category.name),
                reply_markup=vote_keyboard
            )
        else:
            await callback.original.answer(text=msg.DELETE_CATEGORY_REGECT.format(category.name))


class DeleteCategoryAfterVoteCallbackHandler(TelegramCallbackHandler, GeneralCategoryHandler):
    MARKER = DeleteCategoryCallbackHandler.MARKER + markup.VOTE_MARK

    def __init__(self, category_service: CategoryService):
        TelegramCallbackHandler.__init__(self)
        GeneralCategoryHandler.__init__(self, category_service)

    async def handle_(self, callback: CallbackMeta):
        vote_result = callback.payload[self.MARKER]

        if vote_result != EMPTY_VOTE_RESULT:
            category_id = vote_result
            category = self.category_service.find(category_id)
            self.category_service.delete(category_id)
            await callback.original.answer(msg.DELETE_CATEGORY_DONE.format(category.name))
        else:
            await callback.original.answer(msg.DELETE_CATEGORY_CANCEL)

        await self._show_categories_menu(callback.original.message, callback.user_id)
