import os

import telebot
from flask import Flask, request

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
from app.handler.track.track import TrackHandler, TrackAfterVoteCallbackHandler, TrackPostTimeAnswerHandler
from app.handler.user.time_zone import TimeZoneHandler, ChangeTimeZoneCallbackHandler, ChangeTimeZoneHandler
from app.service.activity import ActivityService
from app.service.category import CategoryService
from app.service.event import EventService
from app.service.statistics import StatisticsService
from app.service.user import UserService

server = Flask(__name__)
bot = telebot.TeleBot(config.BOT_API_KEY, parse_mode="MARKDOWN")

categories = CategoryService()
activities = ActivityService()
events = EventService()
user_service = UserService()
statistics_service = StatisticsService()

#### CALLBACK ####
delete_category_before_vote_callback_handler = DeleteCategoryBeforeVoteCallbackHandler(bot, categories, activities)
delete_category_after_vote_callback_handler = DeleteCategoryAfterVoteCallbackHandler(bot, categories)

delete_activity_before_vote_callback_handler = DeleteActivityBeforeVoteCallbackHandler(bot)
delete_activity_after_vote_callback_handler = DeleteActivityAfterVoteCallbackHandler(bot, activities)

track_post_time_answer_handler = TrackPostTimeAnswerHandler(bot, events)
track_after_vote_callback_handler = TrackAfterVoteCallbackHandler(bot, track_post_time_answer_handler)

start_tracking_after_vote_callback_handler = StartTrackingAfterVoteCallbackHandler(bot, events)
stop_tracking_after_vote_callback_handler = StopTrackingAfterVoteCallbackHandler(bot, events)

delete_event_before_events_vote_callback_handler = DeleteEventBeforeEventsVoteCallbackHandler(bot, statistics_service)
delete_event_before_vote_callback_handler = DeleteEventBeforeVoteCallbackHandler(bot, statistics_service)
delete_event_after_vote_callback_handler = DeleteEventAfterVoteCallbackHandler(bot, events)

change_time_zone_handler = ChangeTimeZoneHandler(bot, user_service)
change_time_zone_callback_handler = ChangeTimeZoneCallbackHandler(bot, change_time_zone_handler)

callback_router = CallbackRouter([
    delete_category_before_vote_callback_handler,
    delete_category_after_vote_callback_handler,
    delete_activity_before_vote_callback_handler,
    delete_activity_after_vote_callback_handler,
    track_after_vote_callback_handler,
    start_tracking_after_vote_callback_handler,
    stop_tracking_after_vote_callback_handler,
    delete_event_before_events_vote_callback_handler,
    delete_event_before_vote_callback_handler,
    delete_event_after_vote_callback_handler,
    change_time_zone_callback_handler
]
)

#### HANDLERS ####
start_handler = StartHandler(bot)
# category
categories_handler = CategoriesHandler(bot, categories)
add_category_post_answer_handler = AddCategoryPostAnswerHandler(bot, categories)
add_category_handler = AddCategoryHandler(bot, add_category_post_answer_handler)
delete_category_handler = DeleteCategoryHandler(bot, categories)
# activity
activities_handler = ActivitiesHandler(bot, activities)
add_activity_post_answer_handler = AddActivityPostAnswerHandler(bot, activities)
add_activity_handler = AddActivityHandler(bot, add_activity_post_answer_handler)
delete_activity_handler = DeleteActivityHandler(bot, activities)
# track
track_handler = TrackHandler(bot, activities)
start_tracking_handler = StartTrackingHandler(bot, activities)
stop_tracking_handler = StopTrackingHandler(bot, activities, stop_tracking_after_vote_callback_handler)
last_events_post_answer_handler = LastEventsPostAnswerHandler(bot, activities, statistics_service)
last_events_handler = LastEventsHandler(bot, activities, last_events_post_answer_handler)
delete_event_handler = DeleteEventHandler(bot, activities)
# statistics
statistics_post_answer_handler = StatisticsPostAnswerHandler(bot, statistics_service)
statistics_handler = StatisticsHandler(bot, statistics_post_answer_handler)
# user
time_zone_handler = TimeZoneHandler(bot, user_service)


@bot.message_handler(commands=['start', 'help'])
def main(message):
    start_handler.handle(message)


#################################
#       GENERAL CALLBACK        #
#################################

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    callback_router.route(call)


#########################
#       ACTIVITY        #
#########################

@bot.message_handler(commands=['add_activity'])
def add_activity(message):
    add_activity_handler.handle(message)


@bot.message_handler(commands=['delete_activity'])
def delete_activity(message):
    delete_activity_handler.handle(message)


@bot.message_handler(commands=['activities'])
def activities_(message):
    activities_handler.handle(message)


#########################
#       CATEGORY        #
#########################

@bot.message_handler(commands=['add_category'])
def add_category(message):
    add_category_handler.handle(message)


@bot.message_handler(commands=['delete_category'])
def delete_category(message):
    delete_category_handler.handle(message)


@bot.message_handler(commands=['categories'])
def categories_(message):
    categories_handler.handle(message)


######################
#       TRACK        #
######################

@bot.message_handler(commands=['track'])
def track(message):
    track_handler.handle(message)


@bot.message_handler(commands=['start_tracking'])
def start_tracking(message):
    start_tracking_handler.handle(message)


@bot.message_handler(commands=['stop_tracking'])
def start_tracking(message):
    stop_tracking_handler.handle(message)


######################
#       EVENT        #
######################

@bot.message_handler(commands=['last_events'])
def last_events(message):
    last_events_handler.handle(message)


@bot.message_handler(commands=['delete_event'])
def last_events(message):
    delete_event_handler.handle(message)


#####################
#       USER        #
#####################


@bot.message_handler(commands=['time_zone'])
def time_zone(message):
    time_zone_handler.handle(message)


#######################
#       REPORT        #
#######################

@bot.message_handler(commands=['statistics'])
def statistics(message):
    statistics_handler.handle(message)


##############################
#       APP LAUNCHING        #
##############################


@server.route('/' + config.BOT_API_KEY, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=config.WEBHOOK_URL + config.BOT_API_KEY)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
