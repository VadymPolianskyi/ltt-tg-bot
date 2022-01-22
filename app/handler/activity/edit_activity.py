from aiogram import Dispatcher

from app.config import msg, marker
from app.handler.activity.activity import GeneralActivityHandler
from app.handler.general import TelegramCallbackHandler, TelegramMessageHandler, MessageMeta, CallbackMeta
from app.service import markup
from app.service.activity import ActivityService
from app.service.category import CategoryService
from app.state import EditActivityState


# NAME

class EditActivityNameCallbackHandler(TelegramCallbackHandler):
    MARKER = marker.EDIT_ACTIVITY_NAME

    def __init__(self, activity_service: ActivityService):
        super().__init__()
        self.activity_service = activity_service

    async def handle_(self, callback: CallbackMeta):
        activity = self.activity_service.find(callback.payload[self.MARKER])

        await callback.original.message.answer(msg.EDIT_ACTIVITY_NAME.format(activity.name))
        await EditActivityState.waiting_for_activity_name.set()
        await Dispatcher.get_current().current_state().update_data(activity_id=activity.id)


class EditActivityNameAfterAnswerHandler(TelegramMessageHandler, GeneralActivityHandler):
    def __init__(self, activity_service: ActivityService):
        TelegramCallbackHandler.__init__(self)
        GeneralActivityHandler.__init__(self, activity_service)

    async def handle_(self, message: MessageMeta, *args):
        activity_id = (await Dispatcher.get_current().current_state().get_data())['activity_id']

        activity = self.activity_service.find(activity_id)
        new_name = message.text
        old_name = activity.name

        activity.name = new_name

        self.activity_service.update(activity)

        await message.original.answer(msg.EDIT_ACTIVITY_NAME_DONE.format(old_name, new_name))
        await self._show_activity_settings_menu(message.original, activity)


# CATEGORY

class EditActivityCategoryCallbackHandler(TelegramCallbackHandler):
    MARKER = marker.EDIT_ACTIVITY_CATEGORY

    def __init__(self, activity_service: ActivityService, category_service: CategoryService):
        super().__init__()
        self.activity_service = activity_service
        self.category_service = category_service

    async def handle_(self, callback: CallbackMeta):
        activity = self.activity_service.find(callback.payload[self.MARKER])

        all_categories_markup = self.category_service.create_all_categories_markup(
            marker=EditActivityCategoryAfterAnswerCallbackHandler.MARKER,
            user_id=callback.user_id,
            back_button_marker=marker.ACTIVITY_SETTINGS,
            back_button_value=activity.id
        )

        await callback.original.message.answer(msg.EDIT_ACTIVITY_CATEGORY.format(activity.name),
                                               reply_markup=all_categories_markup)
        await Dispatcher.get_current().current_state().update_data(activity_id=activity.id)


class EditActivityCategoryAfterAnswerCallbackHandler(TelegramCallbackHandler, GeneralActivityHandler):
    MARKER = 'ecacta'

    def __init__(self, activity_service: ActivityService, category_service: CategoryService):
        TelegramCallbackHandler.__init__(self)
        GeneralActivityHandler.__init__(self, activity_service)
        self.category_service = category_service

    async def handle_(self, callback: CallbackMeta):
        activity_id = (await Dispatcher.get_current().current_state().get_data())['activity_id']
        activity = self.activity_service.find(activity_id)
        new_category = self.category_service.find(callback.payload[self.MARKER])

        activity.category_id = new_category.id
        self.activity_service.update(activity)

        await callback.original.message.answer(msg.EDIT_ACTIVITY_CATEGORY_DONE.format(activity.name, new_category.name))
        await Dispatcher.get_current().current_state().finish()

        await self._show_activity_settings_menu(callback.original.message, activity)
