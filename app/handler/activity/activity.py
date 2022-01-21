from aiogram.types import Message

from app.config import msg
from app.db.entity import Activity
from app.service.activity import ActivityService


class GeneralActivityHandler:
    def __init__(self, activity_service: ActivityService):
        self.activity_service = activity_service

    async def _show_activity_settings_menu(self, original_message: Message, activity: Activity):
        activity_settings_keyboard = self.activity_service.create_settings_markup(activity.id, activity.category_id)
        await original_message.answer(msg.ACTIVITY_SETTINGS.format(activity.name),
                                      reply_markup=activity_settings_keyboard)
