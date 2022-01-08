from telebot import TeleBot

from app.config import msg
from app.handler.general import TelegramMessageHandler, MessageMeta
from app.service import ActivityService, StatisticsService


class LastEventsPostAnswerHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService, statistics_service: StatisticsService):
        print('Creating LastEventsPostAnswerHandler...')
        super().__init__(bot)
        self.activities = activities
        self.statistics_service = statistics_service

    def handle_(self, message: MessageMeta, *args):
        answ: str = message.text

        num_limit: int = int(answ) if answ.isnumeric() else 20

        last_events_statistics: list = self.statistics_service.last_events_statistics(message.user_id, num_limit)
        printed_last_events_statistics: str = '\n'.join(
            [s.to_str(with_single_date=True, with_counter=False, prefix=msg.LAST_EVENTS_LIST_PREFIX) for s in
             last_events_statistics])

        self.bot.send_message(message.user_id, msg.LAST_EVENTS_2.format(num_limit, printed_last_events_statistics))


class LastEventsHandler(TelegramMessageHandler):
    def __init__(self, bot: TeleBot, activities: ActivityService,
                 last_events_post_answer_handler: TelegramMessageHandler):
        print('Creating LastEventsHandler...')
        super().__init__(bot)
        self.last_events_post_answer_handler = last_events_post_answer_handler
        self.activities = activities

    def handle_(self, message: MessageMeta, *args):
        self.bot.send_message(message.user_id, msg.LAST_EVENTS_1)
        self.bot.register_next_step_handler_by_chat_id(message.user_id, self.last_events_post_answer_handler.handle)
