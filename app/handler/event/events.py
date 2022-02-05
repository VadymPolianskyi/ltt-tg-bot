from aiogram import Dispatcher

from app.config import msg, marker
from app.handler.activity.activity import GeneralActivityHandler
from app.handler.general import TelegramCallbackHandler, CallbackMeta
from app.service import markup, time_service
from app.service.activity import ActivityService
from app.service.event import EventService
from app.service.markup import EMPTY_VOTE_RESULT
from app.service.statistics import StatisticsService


class ListEventsCallbackHandler(TelegramCallbackHandler):
    MARKER = marker.LIST_EVENTS
    ONE_PAGE_LIMIT = 8

    def __init__(self, activity_service: ActivityService, statistics_service: StatisticsService):
        super().__init__()
        self.activity_service = activity_service
        self.statistics_service = statistics_service

    async def handle_(self, callback: CallbackMeta):
        if self.MARKER in callback.payload.keys():
            activity_id = callback.payload[self.MARKER]
            await Dispatcher.get_current().current_state().finish()
        else:
            activity_id = (await Dispatcher.get_current().current_state().get_data())['activity_id']

        activity = self.activity_service.find(activity_id)

        data = await Dispatcher.get_current().current_state().get_data()
        after_event_id = data['event_id'] if 'event_id' in data.keys() else None

        statistics_with_id = self.statistics_service.statistics_with_event_id(
            user_id=callback.user_id,
            activity_id=activity_id,
            limit=self.ONE_PAGE_LIMIT,
            after_event_id=after_event_id
        )

        buttons = list()
        for s_i in statistics_with_id:
            button_name = f'{msg.DELETE_SIGN} {s_i[1].from_date} - {time_service.minutes_to_str_time(s_i[1].spent_minutes) }'
            end_event_id = s_i[0]
            element = (button_name, DeleteEventBeforeVoteCallbackHandler.MARKER, end_event_id)
            buttons.append(element)

        need_next = len(statistics_with_id) >= 8
        if need_next:
            last_event_id = statistics_with_id[-1][0]
            await Dispatcher.get_current().current_state().update_data(event_id=last_event_id, activity_id=activity_id)
            buttons.append((msg.NEXT_BUTTON, DeleteEventBeforeVoteCallbackHandler.MARKER, '_'))

        buttons.append((msg.BACK_BUTTON, marker.ACTIVITY_SETTINGS, activity_id))

        await callback.original.message.answer(msg.EVENT_LIST.format(activity.name),
                                               reply_markup=markup.create_inline_markup_(buttons))


class DeleteEventBeforeVoteCallbackHandler(TelegramCallbackHandler):
    MARKER = 'devl'

    def __init__(self, event_service: EventService, activity_service: ActivityService,
                 statistics_service: StatisticsService):
        super().__init__()
        self.event_service = event_service
        self.activity_service = activity_service
        self.statistics_service = statistics_service

    async def handle_(self, callback: CallbackMeta):
        input_data: str = callback.payload[self.MARKER]

        if input_data == '_':
            await ListEventsCallbackHandler(self.activity_service, self.statistics_service) \
                .handle_(callback)
        else:
            event = self.event_service.find(input_data)
            vote_keyboard = markup.create_voter_inline_markup(self.MARKER, event.id)

            await Dispatcher.get_current().current_state().update_data(activity_id=event.activity_id)
            await callback.original.message.answer(msg.DELETE_EVENT_VOTE, reply_markup=vote_keyboard)


class DeleteEventAfterVoteCallbackHandler(TelegramCallbackHandler, GeneralActivityHandler):
    MARKER = DeleteEventBeforeVoteCallbackHandler.MARKER + markup.VOTE_MARK

    def __init__(self, activity_service: ActivityService, event_service: EventService):
        TelegramCallbackHandler.__init__(self)
        GeneralActivityHandler.__init__(self, activity_service)
        self.event_service = event_service

    async def handle_(self, callback: CallbackMeta):
        vote_result: str = callback.payload[self.MARKER]

        if vote_result != EMPTY_VOTE_RESULT:
            event_id = vote_result
            self.event_service.delete_pair(event_id)
            await callback.original.answer(msg.DELETE_EVENT_DONE)
        else:
            await callback.original.answer(msg.DELETE_EVENT_CANCELED)

        activity_id = (await Dispatcher.get_current().current_state().get_data())['activity_id']
        activity = self.activity_service.find(activity_id)
        await self._show_activity_settings_menu(callback.original.message, activity)
