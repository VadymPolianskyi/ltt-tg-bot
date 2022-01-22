from aiogram.types import Message

from app.config import msg, marker
from app.db.entity import Activity
from app.service import markup
from app.service.activity import ActivityService


class GeneralActivityHandler:
    def __init__(self, activity_service: ActivityService):
        self.activity_service = activity_service

    async def _show_activity_settings_menu(self, original_message: Message, activity: Activity):
        activity_settings_keyboard = markup.create_inline_markup_([
            (msg.LIST_EVENTS_BUTTON, marker.LIST_EVENTS, activity.id),
            (msg.EDIT_NAME_BUTTON, marker.EDIT_ACTIVITY_NAME, activity.id),
            (msg.CHANGE_CATEGORY_BUTTON, marker.EDIT_ACTIVITY_CATEGORY, activity.id),
            (msg.DELETE_BUTTON, marker.DELETE_ACTIVITY, activity.id),
            (msg.BACK_BUTTON, marker.CATEGORY, activity.category_id)
        ])

        await original_message.answer(msg.ACTIVITY_SETTINGS.format(activity.name),
                                      reply_markup=activity_settings_keyboard)
