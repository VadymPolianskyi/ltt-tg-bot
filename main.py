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
from app.handler.event.events import ListEventsCallbackHandler, DeleteEventBeforeVoteCallbackHandler, \
    DeleteEventAfterVoteCallbackHandler
from app.handler.menu import MenuHandler, MenuCallbackHandler
from app.handler.router import CallbackRouter
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
    TimeZoneWriteTZNameState, EditCategoryState, EditActivityState

bot = Bot(token=config.BOT_API_KEY, parse_mode="Markdown")
dp = Dispatcher(bot, storage=MemoryStorage())

category_service = CategoryService()
activity_service = ActivityService()
event_service = EventService()
user_service = UserService()
statistics_service = StatisticsService()

#### CALLBACK ####

callback_router = CallbackRouter([
    MenuCallbackHandler(activity_service),

    CategoriesCallbackHandler(category_service, activity_service),
    CategoryCallbackHandler(category_service),
    AddCategoryCallbackHandler(),
    SettingsCategoryCallbackHandler(category_service),
    EditCategoryNameCallbackHandler(category_service),
    DeleteCategoryCallbackHandler(category_service, activity_service),
    DeleteCategoryAfterVoteCallbackHandler(category_service),

    AddActivityCallbackHandler(),
    SettingsActivityCallbackHandler(activity_service),
    EditActivityNameCallbackHandler(activity_service),
    EditActivityCategoryCallbackHandler(activity_service, category_service),
    EditActivityCategoryAfterAnswerCallbackHandler(activity_service, category_service),
    DeleteActivityCallbackHandler(activity_service),
    DeleteActivityAfterVoteCallbackHandler(activity_service, category_service),

    StatisticsCallbackHandler(),
    StatisticsPostAnswerCallbackHandler(statistics_service, activity_service),

    StartTrackingCallbackHandler(category_service),
    StartTrackingAfterCategoryCallbackHandler(activity_service),
    StartTrackingAfterActivityCallbackHandler(event_service, activity_service),

    StopTrackingCallbackHandler(activity_service, event_service),
    StopTrackingAfterVoteCallbackHandler(activity_service, event_service),

    TrackCallbackHandler(category_service),
    TrackAfterCategoryCallbackHandler(activity_service),
    TrackAfterActivityCallbackHandler(activity_service),

    ListEventsCallbackHandler(activity_service, statistics_service),
    DeleteEventBeforeVoteCallbackHandler(event_service, activity_service, statistics_service),
    DeleteEventAfterVoteCallbackHandler(activity_service, event_service),

    TimeZoneCallbackHandler(user_service),
    TimeZoneWriteCallbackHandler()
])

#### HANDLERS ####
menu_handler = MenuHandler(activity_service)

# category
add_category_after_answer_handler = AddCategoryAfterAnswerHandler(category_service)
edit_category_name_after_answer_handler = EditCategoryNameAfterAnswerHandler(category_service)

# activity
add_activity_post_answer_handler = AddActivityPostAnswerHandler(activity_service)
edit_activity_name_after_answer_handler = EditActivityNameAfterAnswerHandler(activity_service)

# track
track_after_time_answer_handler = TrackAfterTimeAnswerHandler(activity_service, event_service)

# statistics
statistics_post_answer_handler = StatisticsPostAnswerHandler(statistics_service, activity_service)

# user
change_time_zone_handler = ChangeTimeZoneHandler(user_service)


@dp.message_handler(commands=['start', 'menu'])
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
    executor.start_webhook(
        dispatcher=dp,
        webhook_path='/' + config.BOT_API_KEY,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
    )
