import os

import telebot
from flask import Flask, request

from app.config import config
from app.handler.activity.activities import ActivitiesHandler
from app.handler.activity.add_activity import AddActivityHandler, AddActivityPostAnswerHandler
from app.handler.activity.delete_activity import DeleteActivityHandler, DeleteActivityBeforeVoteCallbackHandler, \
    DeleteActivityAfterVoteCallbackHandler
from app.handler.event.last_event import LastEventsPostAnswerHandler, LastEventsHandler
from app.handler.router import CallbackRouter
from app.handler.start import StartHandler
from app.handler.statistics.statistics import StatisticsHandler, StatisticsPostAnswerHandler
from app.handler.track.start_tracking import StartTrackingHandler, StartTrackingAfterVoteCallbackHandler
from app.handler.track.stop_tracking import StopTrackingAfterVoteCallbackHandler, StopTrackingHandler
from app.handler.track.track import TrackHandler, TrackAfterVoteCallbackHandler, TrackPostTimeAnswerHandler
from app.service import ActivityService, EventService, StatisticsService

server = Flask(__name__)
bot = telebot.TeleBot(config.BOT_API_KEY, parse_mode="MARKDOWN")
activities = ActivityService()
events = EventService()
statistics_service = StatisticsService()

#### CALLBACK ####
delete_activity_before_vote_callback_handler = DeleteActivityBeforeVoteCallbackHandler(bot)
delete_activity_after_vote_callback_handler = DeleteActivityAfterVoteCallbackHandler(bot, activities)

track_post_time_answer_handler = TrackPostTimeAnswerHandler(bot, events)
track_after_vote_callback_handler = TrackAfterVoteCallbackHandler(bot, track_post_time_answer_handler)

start_tracking_after_vote_callback_handler = StartTrackingAfterVoteCallbackHandler(bot, events)
stop_tracking_after_vote_callback_handler = StopTrackingAfterVoteCallbackHandler(bot, events)

callback_router = CallbackRouter(
    delete_activity_before_vote_callback_handler,
    delete_activity_after_vote_callback_handler,
    track_after_vote_callback_handler,
    start_tracking_after_vote_callback_handler,
    stop_tracking_after_vote_callback_handler
)

#### HANDLERS ####
start_handler = StartHandler(bot)
add_activity_post_answer_handler = AddActivityPostAnswerHandler(bot, activities)
add_activity_handler = AddActivityHandler(bot, activities, add_activity_post_answer_handler)
delete_activity_handler = DeleteActivityHandler(bot, activities)
activities_handler = ActivitiesHandler(bot, activities)
track_handler = TrackHandler(bot, activities)
start_tracking_handler = StartTrackingHandler(bot, activities)
stop_tracking_handler = StopTrackingHandler(bot, activities, stop_tracking_after_vote_callback_handler)
last_events_post_answer_handler = LastEventsPostAnswerHandler(bot, activities, statistics_service)
last_events_handler = LastEventsHandler(bot, activities, last_events_post_answer_handler)
statistics_post_answer_handler = StatisticsPostAnswerHandler(bot, statistics_service)
statistics_handler = StatisticsHandler(bot, statistics_post_answer_handler)


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
    bot.set_webhook(url='https://ltt-tg-bot.herokuapp.com/' + config.BOT_API_KEY)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
