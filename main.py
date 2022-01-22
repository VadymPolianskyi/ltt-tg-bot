import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from app.config import config
from app.handler.activity.add_activity import AddActivityCallbackHandler, AddActivityPostAnswerHandler
from app.handler.activity.delete_activity import DeleteActivityAfterVoteCallbackHandler, DeleteActivityCallbackHandler
from app.handler.activity.edit_activity import EditActivityNameCallbackHandler, EditActivityNameAfterAnswerHandler, \
    EditActivityCategoryCallbackHandler, EditActivityCategoryAfterAnswerCallbackHandler
from app.handler.activity.settings_activity import SettingsActivityCallbackHandler
from app.handler.category.add_category import AddCategoryAfterAnswerHandler, AddCategoryCallbackHandler
from app.handler.category.category import CategoriesCallbackHandler, CategoryCallbackHandler
from app.handler.category.delete_category import DeleteCategoryCallbackHandler, \
    DeleteCategoryAfterVoteCallbackHandler
from app.handler.category.edit_category import EditCategoryNameAfterAnswerHandler, EditCategoryNameCallbackHandler
from app.handler.category.settings_category import SettingsCategoryCallbackHandler
from app.handler.event.delete_event import DeleteEventHandler, DeleteEventBeforeEventsVoteCallbackHandler, \
    DeleteEventBeforeVoteCallbackHandler, DeleteEventAfterVoteCallbackHandler
from app.handler.event.last_event import LastEventsPostAnswerHandler, LastEventsHandler
from app.handler.menu import MenuHandler, MenuCallbackHandler
from app.handler.router import CallbackRouter
from app.handler.start import StartHandler
from app.handler.statistics.statistics import StatisticsPostAnswerHandler, StatisticsPostAnswerCallbackHandler, \
    StatisticsCallbackHandler
from app.handler.track.start_tracking import StartTrackingCallbackHandler, StartTrackingAfterCategoryCallbackHandler, \
    StartTrackingAfterActivityCallbackHandler
from app.handler.track.stop_tracking import StopTrackingAfterVoteCallbackHandler, StopTrackingCallbackHandler
from app.handler.track.track import TrackAfterTimeAnswerHandler, TrackCallbackHandler, \
    TrackAfterCategoryCallbackHandler, TrackAfterActivityCallbackHandler
from app.handler.user.time_zone import ChangeTimeZoneHandler, TimeZoneCallbackHandler, TimeZoneWriteCallbackHandler
from app.service.activity import ActivityService
from app.service.category import CategoryService
from app.service.event import EventService
from app.service.statistics import StatisticsService
from app.service.user import UserService
from app.state import CreateActivityState, CreateCategoryState, TrackWriteTimeRangeState, StatisticWriteTimeRangeState, \
    TimeZoneWriteTZNameState, LastEventsWriteCountState, EditCategoryState, EditActivityState

bot = Bot(token=config.BOT_API_KEY, parse_mode="Markdown")
dp = Dispatcher(bot, storage=MemoryStorage())

categories = CategoryService()
activities = ActivityService()
events = EventService()
user_service = UserService()
statistics_service = StatisticsService()

#### CALLBACK ####

callback_router = CallbackRouter([
    MenuCallbackHandler(),

    CategoriesCallbackHandler(categories, activities),
    CategoryCallbackHandler(categories),
    AddCategoryCallbackHandler(),
    SettingsCategoryCallbackHandler(categories),
    EditCategoryNameCallbackHandler(categories),
    DeleteCategoryCallbackHandler(categories, activities),
    DeleteCategoryAfterVoteCallbackHandler(categories),

    AddActivityCallbackHandler(),
    SettingsActivityCallbackHandler(activities),
    EditActivityNameCallbackHandler(activities),
    EditActivityCategoryCallbackHandler(activities, categories),
    EditActivityCategoryAfterAnswerCallbackHandler(activities, categories),
    DeleteActivityCallbackHandler(activities),
    DeleteActivityAfterVoteCallbackHandler(activities, categories),

    StatisticsCallbackHandler(),
    StatisticsPostAnswerCallbackHandler(statistics_service),

    StartTrackingCallbackHandler(categories),
    StartTrackingAfterCategoryCallbackHandler(activities),
    StartTrackingAfterActivityCallbackHandler(events),

    StopTrackingCallbackHandler(activities, events),
    StopTrackingAfterVoteCallbackHandler(activities, events),

    TrackCallbackHandler(categories),
    TrackAfterCategoryCallbackHandler(activities),
    TrackAfterActivityCallbackHandler(activities),

    DeleteEventBeforeEventsVoteCallbackHandler(statistics_service),
    DeleteEventBeforeVoteCallbackHandler(statistics_service),
    DeleteEventAfterVoteCallbackHandler(events),

    TimeZoneCallbackHandler(user_service),
    TimeZoneWriteCallbackHandler()
])

#### HANDLERS ####
start_handler = StartHandler()
menu_handler = MenuHandler()

# category
add_category_after_answer_handler = AddCategoryAfterAnswerHandler(categories)
edit_category_name_after_answer_handler = EditCategoryNameAfterAnswerHandler(categories)

# activity
add_activity_post_answer_handler = AddActivityPostAnswerHandler(activities)
edit_activity_name_after_answer_handler = EditActivityNameAfterAnswerHandler(activities)

# track
track_after_time_answer_handler = TrackAfterTimeAnswerHandler(activities, events)

# event
last_events_post_answer_handler = LastEventsPostAnswerHandler(activities, statistics_service)
last_events_handler = LastEventsHandler(activities)
delete_event_handler = DeleteEventHandler(activities)

# statistics
statistics_post_answer_handler = StatisticsPostAnswerHandler(statistics_service)

# user
change_time_zone_handler = ChangeTimeZoneHandler(user_service)


@dp.message_handler(commands=['start', 'help'])
async def start(message):
    await start_handler.handle(message)


@dp.message_handler(commands=['menu'])
async def menu(message):
    await menu_handler.handle(message)


#################################
#       GENERAL CALLBACK        #
#################################

@dp.callback_query_handler(state="*")
async def callback_handler(call):
    await callback_router.route(call)


#########################
#       ACTIVITY        #
#########################


@dp.message_handler(state=CreateActivityState.waiting_for_activity_name)
async def add_activity_post_answer(message, state: FSMContext):
    await add_activity_post_answer_handler.handle(message)
    await state.finish()


@dp.message_handler(state=EditActivityState.waiting_for_activity_name)
async def edit_activity_name_after_answer(message, state: FSMContext):
    await edit_activity_name_after_answer_handler.handle(message)
    await state.finish()


#########################
#       CATEGORY        #
#########################

@dp.message_handler(state=CreateCategoryState.waiting_for_category_name)
async def add_category_post_answer(message, state: FSMContext):
    await add_category_after_answer_handler.handle(message)
    await state.finish()


@dp.message_handler(state=EditCategoryState.waiting_for_category_name)
async def edit_category_name_after_answer(message, state: FSMContext):
    await edit_category_name_after_answer_handler.handle(message)
    await state.finish()


######################
#       TRACK        #
######################

@dp.message_handler(state=TrackWriteTimeRangeState.waiting_for_time_range)
async def track_(message, state: FSMContext):
    await track_after_time_answer_handler.handle(message)
    await state.finish()


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


@dp.message_handler(state=TimeZoneWriteTZNameState.waiting_for_time_zone_name)
async def time_zone_after_answer(message):
    await change_time_zone_handler.handle(message)


#######################
#       REPORT        #
#######################

@dp.message_handler(state=StatisticWriteTimeRangeState.waiting_for_time_range)
async def statistics_post_time_answer(message, state: FSMContext):
    await statistics_post_answer_handler.handle(message)
    await state.finish()


##############################
#       APP LAUNCHING        #
##############################


async def on_startup(_):
    await bot.set_webhook(config.WEBHOOK_URL + config.BOT_API_KEY)


async def on_shutdown(dp):
    print('Shutting down..')

    await bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()

    print('Bye!')


if __name__ == "__main__":
    # executor.start_webhook(
    #     dispatcher=dp,
    #     webhook_path='/' + config.BOT_API_KEY,
    #     on_startup=on_startup,
    #     on_shutdown=on_shutdown,
    #     skip_updates=True,
    #     host=config.SERVER_HOST,
    #     port=config.SERVER_PORT,
    # )
    asyncio.run(executor.start_polling(dispatcher=dp))
