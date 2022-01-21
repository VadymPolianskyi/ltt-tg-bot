from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta
from app.service.activity import ActivityService


class ActivitiesHandler(TelegramMessageHandler):
    def __init__(self, activities: ActivityService):
        print('Creating ActivitiesHandler...')
        super().__init__()
        self.activities = activities

    async def handle_(self, message: MessageMeta, *args):
        all_activity_titles = self.activities.show_all_titles(message.user_id)
        str_list = "\n- " + "\n- ".join(all_activity_titles) if all_activity_titles else "\n Nothing yet..."

        await message.original.answer(msg.ALL_ACTIVITIES.format(str_list))
