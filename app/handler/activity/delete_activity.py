from aiogram import Dispatcher

from app.config import msg, marker
from app.handler.activity.activity import GeneralActivityHandler
from app.handler.category.category import GeneralCategoryHandler
from app.handler.general import TelegramCallbackHandler, CallbackMeta
from app.service import markup
from app.service.activity import ActivityService
from app.service.category import CategoryService
from app.service.markup import EMPTY_VOTE_RESULT


class DeleteActivityCallbackHandler(TelegramCallbackHandler):
    MARKER = marker.DELETE_ACTIVITY

    def __init__(self, activity_service: ActivityService):
        super().__init__()
        self.activity_service = activity_service

    async def handle_(self, callback: CallbackMeta):
        activity = self.activity_service.find(callback.payload[self.MARKER])

        vote_keyboard = markup.create_voter_inline_markup(self.MARKER, activity.id)
        await callback.original.message.answer(
            text=msg.DELETE_ACTIVITY_2.format(activity.name),
            reply_markup=vote_keyboard
        )
        await Dispatcher.get_current().current_state().update_data(activity_id=activity.id)


class DeleteActivityAfterVoteCallbackHandler(TelegramCallbackHandler, GeneralActivityHandler, GeneralCategoryHandler):
    MARKER = DeleteActivityCallbackHandler.MARKER + markup.VOTE_MARK

    def __init__(self, activity_service: ActivityService, category_service: CategoryService):
        TelegramCallbackHandler.__init__(self)
        GeneralActivityHandler.__init__(self, activity_service)
        GeneralCategoryHandler.__init__(self, category_service)

    async def handle_(self, callback: CallbackMeta):
        vote_result = callback.payload[self.MARKER]

        if vote_result != EMPTY_VOTE_RESULT:
            activity = self.activity_service.find(vote_result)

            self.activity_service.delete(activity.id)
            await callback.original.message.answer(msg.DELETE_ACTIVITY_3_1.format(activity.name))

            # to category
            category = self.category_service.find(activity.category_id)
            await self._show_category_menu(callback.original.message, category)
        else:
            await callback.original.answer(msg.DELETE_ACTIVITY_4_1)

            activity_id = (await Dispatcher.get_current().current_state().get_data())['activity_id']
            activity = self.activity_service.find(activity_id)
            await self._show_activity_settings_menu(callback.original.message, activity)
