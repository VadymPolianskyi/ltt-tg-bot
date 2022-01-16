from telebot import TeleBot

from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta
from app.service.statistics import StatisticsService


class StatisticsPostAnswerHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, statistics_service: StatisticsService):
        print('Creating StatisticsPostAnswerHandler...')
        super().__init__(bot)
        self.statistics_service = statistics_service

    def handle_(self, message: MessageMeta, *args):
        date_range_inp: str = message.text
        report_message: str = self.statistics_service.generate(message.user_id, date_range_inp).to_str()
        self.bot.send_message(message.user_id, report_message)


class StatisticsHandler(TelegramMessageHandler):
    def __init__(self,
                 bot: TeleBot,
                 statistics_post_answer_handler: TelegramMessageHandler):
        print('Creating StatisticsHandler...')
        super().__init__(bot)
        self.statistics_post_answer_handler = statistics_post_answer_handler

    def handle_(self, message: MessageMeta, *args):
        self.bot.send_message(chat_id=message.user_id, text=msg.STATISTIC_1)
        self.bot.register_next_step_handler_by_chat_id(message.user_id, self.statistics_post_answer_handler.handle)
