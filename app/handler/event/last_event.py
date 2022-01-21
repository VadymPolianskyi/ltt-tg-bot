from app import state
from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta
from app.service.activity import ActivityService
from app.service.statistics import StatisticsService


class LastEventsHandler(TelegramMessageHandler):
    def __init__(self, activities: ActivityService):
        super().__init__()
        self.activities = activities

    async def handle_(self, message: MessageMeta, *args):
        await message.original.answer(msg.LAST_EVENTS_1)
        await state.LastEventsWriteCountState.waiting_for_count.set()


class LastEventsPostAnswerHandler(TelegramMessageHandler):
    def __init__(self, activities: ActivityService, statistics_service: StatisticsService):
        super().__init__()
        self.activities = activities
        self.statistics_service = statistics_service

    async def handle_(self, message: MessageMeta, *args):
        answ: str = message.text

        num_limit: int = int(answ) if answ.isnumeric() else 20

        last_events_statistics: list = self.statistics_service.last_events_statistics(message.user_id, num_limit)
        printed_last_events_statistics: str = '\n'.join(
            [s.to_str(with_single_date=True, with_counter=False, prefix=msg.LAST_EVENTS_LIST_PREFIX) for s in
             last_events_statistics])

        await message.original.answer(msg.LAST_EVENTS_2.format(num_limit, printed_last_events_statistics))
