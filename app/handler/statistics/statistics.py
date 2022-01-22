import time

from aiogram import Dispatcher

from app.config import msg, marker
from app.handler.general import TelegramMessageHandler, MessageMeta, TelegramCallbackHandler, CallbackMeta
from app.handler.menu import MenuGeneral
from app.service import markup
from app.service.activity import ActivityService
from app.service.statistics import StatisticsService
from app.state import StatisticWriteTimeRangeState


class StatisticsCallbackHandler(TelegramCallbackHandler):
    MARKER = marker.STATISTICS

    def __init__(self):
        super().__init__()

    async def handle_(self, call: CallbackMeta):
        markup_buttons = [
            ('Today', StatisticsPostAnswerCallbackHandler.MARKER, '1d'),
            ('Last 2 days', StatisticsPostAnswerCallbackHandler.MARKER, '2d'),
            ('Last week', StatisticsPostAnswerCallbackHandler.MARKER, '1w'),
            ('Last 2 weeks', StatisticsPostAnswerCallbackHandler.MARKER, '2w'),
            ('Last 30 days', StatisticsPostAnswerCallbackHandler.MARKER, '30d'),
            (msg.BACK_BUTTON, marker.MENU, '_'),
        ]
        time_range_markup = markup.create_inline_markup_(markup_buttons)

        sent_msg = await call.original.message.answer(msg.STATISTIC_PERIOD, reply_markup=time_range_markup)
        await StatisticWriteTimeRangeState.waiting_for_time_range.set()
        await Dispatcher.get_current().current_state().update_data(message_id=sent_msg.message_id)


class StatisticsPostAnswerCallbackHandler(TelegramCallbackHandler, MenuGeneral):
    MARKER = 'stp'

    def __init__(self, statistics_service: StatisticsService, activity_service: ActivityService):
        TelegramCallbackHandler.__init__(self)
        MenuGeneral.__init__(self, activity_service)
        self.statistics_service = statistics_service

    async def handle_(self, call: CallbackMeta):
        period = call.payload[self.MARKER]

        report_message: str = self.statistics_service.generate(
            user_id=call.user_id,
            user_time_zone=str(call.time.tzinfo),
            date_range=period
        ).to_str()

        await call.original.message.answer(report_message)
        time.sleep(1)
        await self._show_menu(call.original.message, call.user_id)


class StatisticsPostAnswerHandler(TelegramMessageHandler, MenuGeneral):
    def __init__(self, statistics_service: StatisticsService, activity_service: ActivityService):
        TelegramMessageHandler.__init__(self)
        MenuGeneral.__init__(self, activity_service)
        self.statistics_service = statistics_service

    async def handle_(self, message: MessageMeta, *args):
        message_id = (await Dispatcher.get_current().current_state().get_data())['message_id']
        await message.original.bot.delete_message(message.user_id, message_id)

        report_message: str = self.statistics_service.generate(
            user_id=message.user_id,
            user_time_zone=str(message.time.tzinfo),
            date_range=message.text
        ).to_str()

        await message.original.answer(report_message)
        time.sleep(1)
        await self._show_menu(message.original)
