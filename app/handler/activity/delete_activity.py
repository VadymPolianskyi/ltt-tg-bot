from app.config import msg
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler, MessageMeta, CallbackMeta
from app.service import markup
from app.service.activity import ActivityService
from app.service.markup import EMPTY_VOTE_RESULT


class DeleteActivityHandler(TelegramMessageHandler):
    def __init__(self, activities: ActivityService):
        print('Creating DeleteActivityHandler...')
        super().__init__()
        self.activities = activities

    async def handle_(self, message: MessageMeta, *args):
        all_user_activity_titles = self.activities.show_all_titles(message.user_id)
        activities_keyboard = markup.create_simple_inline_markup(
            DeleteActivityBeforeVoteCallbackHandler.MARKER,
            all_user_activity_titles
        )

        await message.original.answer(msg.DELETE_ACTIVITY_1, reply_markup=activities_keyboard)


class DeleteActivityBeforeVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'delete'

    def __init__(self):
        print('Creating DeleteActivityBeforeVoteCallbackHandler...')
        super().__init__()

    async def handle_(self, callback: CallbackMeta):
        activity_name = callback.payload[self.MARKER]

        vote_keyboard = markup.create_voter_inline_markup(self.MARKER, activity_name)
        await callback.original.message.answer(
            text=msg.DELETE_ACTIVITY_2.format(activity_name),
            reply_markup=vote_keyboard
        )


class DeleteActivityAfterVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = DeleteActivityBeforeVoteCallbackHandler.MARKER + markup.VOTE_MARK

    def __init__(self, activities: ActivityService):
        print('Creating DeleteActivityAfterVoteCallbackHandler...')
        super().__init__()
        self.activities = activities

    async def handle_(self, callback: CallbackMeta):
        vote_result = callback.payload[self.MARKER]

        if vote_result != EMPTY_VOTE_RESULT:
            activity_name = vote_result
            self.activities.delete(callback.user_id, activity_name)
            await callback.original.message.answer(msg.DELETE_ACTIVITY_3_1.format(activity_name))
        else:
            await callback.original.message.answer(msg.DELETE_ACTIVITY_4_1)
