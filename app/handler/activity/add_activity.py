from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta
from app.service.activity import ActivityService


class AddActivityHandler(TelegramMessageHandler):
    def __init__(self):
        print('Creating AddActivityHandler...')
        super().__init__()

    async def handle_(self, message: MessageMeta, *args):
        await message.original.answer(msg.ADD_ACTIVITY_1)


class AddActivityPostAnswerHandler(TelegramMessageHandler):
    def __init__(self, activities: ActivityService):
        print('Creating AddActivityPostAnswerHandler...')
        super().__init__()
        self.activities = activities

    async def handle_(self, message: MessageMeta, *args):
        activity_name = message.text
        activity = self.activities.create(message.user_id, activity_name)

        await message.original.answer(msg.ADD_ACTIVITY_2.format(activity.name))
