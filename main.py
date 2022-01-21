from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from app.config import config
from app.handler.activity.activities import ActivitiesHandler
from app.handler.activity.add_activity import AddActivityHandler, AddActivityPostAnswerHandler
from app.handler.activity.delete_activity import DeleteActivityHandler, DeleteActivityBeforeVoteCallbackHandler, \
    DeleteActivityAfterVoteCallbackHandler
from app.handler.category.add_category import AddCategoryPostAnswerHandler, AddCategoryHandler
from app.handler.category.categories import CategoriesHandler
from app.handler.category.delete_category import DeleteCategoryHandler, DeleteCategoryBeforeVoteCallbackHandler, \
    DeleteCategoryAfterVoteCallbackHandler
from app.handler.event.delete_event import DeleteEventHandler, DeleteEventBeforeEventsVoteCallbackHandler, \
    DeleteEventBeforeVoteCallbackHandler, DeleteEventAfterVoteCallbackHandler
from app.handler.event.last_event import LastEventsPostAnswerHandler, LastEventsHandler
from app.handler.router import CallbackRouter
from app.handler.start import StartHandler
from app.handler.statistics.statistics import StatisticsHandler, StatisticsPostAnswerHandler
from app.handler.track.start_tracking import StartTrackingHandler, StartTrackingAfterVoteCallbackHandler
from app.handler.track.stop_tracking import StopTrackingAfterVoteCallbackHandler, StopTrackingHandler
from app.handler.track.track import TrackHandler, TrackAfterChoiseCallbackHandler, TrackAfterTimeAnswerHandler
from app.handler.user.time_zone import TimeZoneHandler, ChangeTimeZoneCallbackHandler, ChangeTimeZoneHandler
from app.service.activity import ActivityService
from app.service.category import CategoryService
from app.service.event import EventService
from app.service.statistics import StatisticsService
from app.service.user import UserService
from app.state import CreateActivityState, CreateCategoryState, TrackWriteTimeRangeState, StatisticWriteTimeRangeState, \
    TimeZoneWriteTZNameState, LastEventsWriteCountState

bot = Bot(token=config.BOT_API_KEY, parse_mode="Markdown")
dp = Dispatcher(bot, storage=MemoryStorage())

categories = CategoryService()
activities = ActivityService()
events = EventService()
user_service = UserService()
statistics_service = StatisticsService()

#### CALLBACK ####
delete_category_before_vote_callback_handler = DeleteCategoryBeforeVoteCallbackHandler(categories, activities)
delete_category_after_vote_callback_handler = DeleteCategoryAfterVoteCallbackHandler(categories)

delete_activity_before_vote_callback_handler = DeleteActivityBeforeVoteCallbackHandler()
delete_activity_after_vote_callback_handler = DeleteActivityAfterVoteCallbackHandler(activities)

track_after_choise_callback_handler = TrackAfterChoiseCallbackHandler()
track_after_time_answer_handler = TrackAfterTimeAnswerHandler(events)

start_tracking_after_vote_callback_handler = StartTrackingAfterVoteCallbackHandler(events)
stop_tracking_after_vote_callback_handler = StopTrackingAfterVoteCallbackHandler(events)

delete_event_before_events_vote_callback_handler = DeleteEventBeforeEventsVoteCallbackHandler(statistics_service)
delete_event_before_vote_callback_handler = DeleteEventBeforeVoteCallbackHandler(statistics_service)
delete_event_after_vote_callback_handler = DeleteEventAfterVoteCallbackHandler(events)

change_time_zone_handler = ChangeTimeZoneHandler(user_service)
change_time_zone_callback_handler = ChangeTimeZoneCallbackHandler()

callback_router = CallbackRouter([
    delete_category_before_vote_callback_handler,
    delete_category_after_vote_callback_handler,
    delete_activity_before_vote_callback_handler,
    delete_activity_after_vote_callback_handler,
    track_after_choise_callback_handler,
    start_tracking_after_vote_callback_handler,
    stop_tracking_after_vote_callback_handler,
    delete_event_before_events_vote_callback_handler,
    delete_event_before_vote_callback_handler,
    delete_event_after_vote_callback_handler,
    change_time_zone_callback_handler
]
)

#### HANDLERS ####
start_handler = StartHandler()
# category
categories_handler = CategoriesHandler(categories)
add_category_post_answer_handler = AddCategoryPostAnswerHandler(categories)
add_category_handler = AddCategoryHandler()
delete_category_handler = DeleteCategoryHandler(categories)
# activity
activities_handler = ActivitiesHandler(activities)
add_activity_handler = AddActivityHandler()
add_activity_post_answer_handler = AddActivityPostAnswerHandler(activities)
delete_activity_handler = DeleteActivityHandler(activities)
# track
track_handler = TrackHandler(activities)
start_tracking_handler = StartTrackingHandler(activities)
stop_tracking_handler = StopTrackingHandler(activities, events)
last_events_post_answer_handler = LastEventsPostAnswerHandler(activities, statistics_service)
last_events_handler = LastEventsHandler(activities)
delete_event_handler = DeleteEventHandler(activities)
# statistics
statistics_post_answer_handler = StatisticsPostAnswerHandler(statistics_service)
statistics_handler = StatisticsHandler()
# user
time_zone_handler = TimeZoneHandler(user_service)


# async def set_commands(bot: Bot):
#     commands = [BotCommand(command="/menu", description="Show menu")]
#     await bot.set_my_commands(commands)


@dp.message_handler(commands=['start', 'help', 'menu'])
async def main(message):
    await start_handler.handle(message)


#################################
#       GENERAL CALLBACK        #
#################################

@dp.callback_query_handler()
async def callback_handler(call):
    await callback_router.route(call)


#########################
#       ACTIVITY        #
#########################

@dp.message_handler(commands=['activities'])
async def activities_(message):
    await activities_handler.handle(message)


@dp.message_handler(commands=['add_activity'])
async def add_activity(message):
    await add_activity_handler.handle(message)
    await CreateActivityState.waiting_for_activity_name.set()


@dp.message_handler(state=CreateActivityState.waiting_for_activity_name)
async def add_activity_post_answer(message, state: FSMContext):
    await add_activity_post_answer_handler.handle(message)
    await state.finish()


@dp.message_handler(commands=['delete_activity'])
async def delete_activity(message):
    await delete_activity_handler.handle(message)


#########################
#       CATEGORY        #
#########################

@dp.message_handler(commands=['categories'])
async def categories_(message):
    await categories_handler.handle(message)


@dp.message_handler(commands=['add_category'])
async def add_category(message):
    await add_category_handler.handle(message)
    await CreateCategoryState.waiting_for_category_name.set()


@dp.message_handler(state=CreateCategoryState.waiting_for_category_name)
async def add_category_post_answer(message, state: FSMContext):
    await add_category_post_answer_handler.handle(message)
    await state.finish()


@dp.message_handler(commands=['delete_category'])
async def delete_category(message):
    await delete_category_handler.handle(message)


######################
#       TRACK        #
######################

@dp.message_handler(commands=['track'])
async def track(message):
    await track_handler.handle(message)


@dp.message_handler(state=TrackWriteTimeRangeState.waiting_for_time_range)
async def track_(message, state: FSMContext):
    await track_after_time_answer_handler.handle(message)
    await state.finish()


@dp.message_handler(commands=['start_tracking'])
async def start_tracking(message):
    await start_tracking_handler.handle(message)


@dp.message_handler(commands=['stop_tracking'])
async def start_tracking(message):
    await stop_tracking_handler.handle(message)


######################
#       EVENT        #
######################

@dp.message_handler(commands=['last_events'])
async def last_events(message):
    await last_events_handler.handle(message)


@dp.message_handler(state=LastEventsWriteCountState.waiting_for_count)
async def last_events_after_count(message, state: FSMContext):
    await last_events_post_answer_handler.handle(message)
    await state.finish()


@dp.message_handler(commands=['delete_event'])
async def delete_event(message):
    await delete_event_handler.handle(message)


#####################
#       USER        #
#####################


@dp.message_handler(commands=['time_zone'])
async def time_zone(message):
    await time_zone_handler.handle(message)


@dp.message_handler(state=TimeZoneWriteTZNameState.waiting_for_time_zone_name)
async def time_zone_after_answer(message):
    await change_time_zone_handler.handle(message)


#######################
#       REPORT        #
#######################

@dp.message_handler(commands=['statistics'])
async def statistics(message):
    await statistics_handler.handle(message)
    await StatisticWriteTimeRangeState.waiting_for_time_range.set()


@dp.message_handler(state=StatisticWriteTimeRangeState.waiting_for_time_range)
async def statistics_post_time_answer(message, state: FSMContext):
    await statistics_post_answer_handler.handle(message)
    await state.finish()


##############################
#       APP LAUNCHING        #
##############################


async def on_startup(_):
    await bot.set_webhook(config.WEBHOOK_URL + '/' + config.BOT_API_KEY)


async def on_shutdown(dp):
    print('Shutting down..')

    await bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    print('Bye!')


if __name__ == "__main__":
    executor.start_webhook(
        dispatcher=dp,
        webhook_path='/' + config.BOT_API_KEY,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
    )
