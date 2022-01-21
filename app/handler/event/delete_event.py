from app.config import msg
from app.handler.general import TelegramMessageHandler, TelegramCallbackHandler, MessageMeta, CallbackMeta
from app.service import markup
from app.service.activity import ActivityService
from app.service.event import EventService
from app.service.markup import EMPTY_VOTE_RESULT
from app.service.statistics import StatisticsService

NEXT = 'next_'


class DeleteEventHandler(TelegramMessageHandler):
    def __init__(self, activities: ActivityService):
        super().__init__()
        self.activities = activities

    async def handle_(self, message: MessageMeta, *args):
        activities_keyboard = self.activities.all_activities_keyboard(
            message.user_id,
            DeleteEventBeforeEventsVoteCallbackHandler.MARKER
        )

        await message.original.answer(msg.DELETE_EVENT_1, reply_markup=activities_keyboard)


class DeleteEventBeforeEventsVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'd_e'
    ONE_PAGE_LIMIT = 9

    def __init__(self, statistics_service: StatisticsService, after_event_id: str = None):
        super().__init__()
        self.statistics_service = statistics_service
        self.after_event_id = after_event_id

    async def handle_(self, callback: CallbackMeta):
        activity_name = callback.payload[self.MARKER] if self.MARKER in callback.payload.keys() else None

        statistics_with_id = self.statistics_service.statistics_with_event_id(
            user_id=callback.user_id,
            activity_name=activity_name,
            limit=self.ONE_PAGE_LIMIT,
            after_event_id=self.after_event_id
        )

        if len(statistics_with_id) == 0 and activity_name:
            await callback.original.message.answer(text=msg.DELETE_EVENT_2_2.format(activity_name))
        else:
            buttons = list()
            for s_i in statistics_with_id:
                element = (f'{s_i[1].from_date} - {s_i[1].format_spent_minutes()}', s_i[0])
                buttons.append(element)

            need_next = len(statistics_with_id) >= 9
            if need_next:
                last_button = ('Next', NEXT + statistics_with_id[-1][0])
                buttons.append(last_button)

            vote_keyboard = markup.create_inline_markup(DeleteEventBeforeVoteCallbackHandler.MARKER, buttons)
            await callback.original.message.answer(
                msg.DELETE_EVENT_2_1.format(activity_name),
                reply_markup=vote_keyboard
            )


class DeleteEventBeforeVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'd_ev'

    def __init__(self, statistics_service: StatisticsService):
        super().__init__()
        self.statistics_service = statistics_service

    async def handle_(self, callback: CallbackMeta):
        event_id: str = callback.payload[self.MARKER]

        if NEXT in event_id:
            await DeleteEventBeforeEventsVoteCallbackHandler(self.statistics_service, event_id.removeprefix(NEXT)) \
                .handle_(callback)
        else:
            vote_keyboard = markup.create_voter_inline_markup(self.MARKER, event_id)
            await callback.original.message.answer(msg.DELETE_EVENT_3, reply_markup=vote_keyboard)


class DeleteEventAfterVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = DeleteEventBeforeVoteCallbackHandler.MARKER + markup.VOTE_MARK

    def __init__(self, events: EventService):
        super().__init__()
        self.events = events

    async def handle_(self, callback: CallbackMeta):
        vote_result: str = callback.payload[self.MARKER]

        if vote_result != EMPTY_VOTE_RESULT:
            event_id = vote_result
            self.events.delete_pair(event_id)
            await callback.original.message.answer(msg.DELETE_EVENT_4_1)
        else:
            await callback.original.message.answer(msg.DELETE_EVENT_5_1)
