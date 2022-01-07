from telebot import TeleBot
from telebot.types import Message

from app.config import msg
from app.handler.general import TelegramMessageHandler
from app.service import StatisticsService


class StatisticsPostAnswerHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, statistics_service: StatisticsService):
        print('Creating StatisticsPostAnswerHandler...')
        super().__init__(bot)
        self.statistics_service = statistics_service

    def handle_(self, message: Message, *args):
        date_range_inp: str = message.text
        report_message: str = self.statistics_service.generate(message.from_user.id, date_range_inp).to_str()
        self.bot.send_message(message.chat.id, report_message)


class StatisticsHandler(TelegramMessageHandler):
    def __init__(self,
                 bot: TeleBot,
                 statistics_post_answer_handler: TelegramMessageHandler):
        print('Creating StatisticsHandler...')
        super().__init__(bot)
        self.statistics_post_answer_handler = statistics_post_answer_handler

    def handle_(self, message: Message, *args):
        self.bot.send_message(chat_id=message.chat.id, text=msg.STATISTIC_1)
        self.bot.register_next_step_handler_by_chat_id(message.chat.id, self.statistics_post_answer_handler.handle)
