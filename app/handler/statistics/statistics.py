from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta
from app.service.statistics import StatisticsService


class StatisticsHandler(TelegramMessageHandler):
    def __init__(self):
        super().__init__()

    async def handle_(self, message: MessageMeta, *args):
        await message.original.answer(msg.STATISTIC_1)


class StatisticsPostAnswerHandler(TelegramMessageHandler):
    def __init__(self, statistics_service: StatisticsService):
        super().__init__()
        self.statistics_service = statistics_service

    async def handle_(self, message: MessageMeta, *args):
        report_message: str = self.statistics_service.generate(
            user_id=message.user_id,
            user_time_zone=str(message.time.tzinfo),
            date_range=message.text
        ).to_str()

        await message.original.answer(report_message)
