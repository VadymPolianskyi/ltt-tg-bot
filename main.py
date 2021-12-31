import json

import telebot
from flask import Flask, request
import os

from app.config import config, msg
from app.db import EventType
from app.service import ActivityService, EventService, StatisticsService
from app.util import time, markup

server = Flask(__name__)
bot = telebot.TeleBot(config.BOT_API_KEY, parse_mode="MARKDOWN")
activities = ActivityService()
events = EventService()
statistics_service = StatisticsService()


@bot.message_handler(commands=['start', 'help'])
def main(message):
    print(f"Message '{message.text}' from @{message.chat.username} in chat({message.chat.id})")
    bot.send_message(message.chat.id, msg.START)


#################################
#       GENERAL CALLBACK        #
#################################

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.from_user.id
    username = call.from_user.username
    message_id = call.message.id

    try:
        callback_inp = json.loads(call.data)

        if 'delete' in callback_inp.keys():
            activity_name = callback_inp['delete']
            __delete_activity_before_vote(chat_id=chat_id, message_id=message_id, activity_name=activity_name)

        if 'delete_vote' in callback_inp.keys():
            activity_name = callback_inp['payload']
            vote = callback_inp['delete_vote']
            __delete_activity_after_vote(chat_id, message_id, username, activity_name, vote)

        if 'delete_event' in callback_inp.keys():
            activity_name = callback_inp['delete_event']
            __delete_last_tracking_before_vote(chat_id, message_id, username, activity_name)

        if 'delete_event_vote' in callback_inp.keys():
            activity_name = callback_inp['payload']
            vote = callback_inp['delete_event_vote']
            __delete_last_tracking_after_vote(chat_id, message_id, vote, username, activity_name)

        if 'clear_vote' in callback_inp.keys():
            vote = callback_inp['clear_vote']
            __clear_after_vote(chat_id, message_id, username, vote)

        if 'track' in callback_inp.keys():
            activity_name = callback_inp['track']
            __track_post_activity_answer(chat_id, message_id, activity_name)

        if 'start_tracking' in callback_inp.keys():
            activity_name = callback_inp['start_tracking']
            __start_tracking_post_answer(chat_id, activity_name, username, message_id)

        if 'stop_tracking' in callback_inp.keys():
            activity_name = callback_inp['stop_tracking']
            __stop_tracking_post_answer(chat_id, activity_name, username, message_id)

    except Exception as e:
        print(e)
        bot.send_message(chat_id, msg.ERROR_BASIC)


#########################
#       ACTIVITY        #
#########################

@bot.message_handler(commands=['add_activity'])
def add_activity(message):
    print(f"Message '{message.text}' from @{message.chat.username} in chat({message.chat.id})")
    try:
        bot.send_message(message.chat.id, msg.ADD_ACTIVITY_1)
        bot.register_next_step_handler_by_chat_id(message.chat.id, __add_activity_post_answer)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


def __add_activity_post_answer(message):
    try:
        activity_name = message.text
        activity = activities.create(message.chat.username, activity_name)

        bot.send_message(message.chat.id, msg.ADD_ACTIVITY_2.format(activity.name))
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


@bot.message_handler(commands=['delete_activity'])
def delete_activity(message):
    print(f"Message '{message.text}' from @{message.chat.username} in chat({message.chat.id})")
    try:
        all_user_activity_titles = activities.show_all_titles(message.chat.username)
        activities_keyboard = markup.create_inline_markup('delete', all_user_activity_titles)

        bot.send_message(message.chat.id, msg.DELETE_ACTIVITY_1, reply_markup=activities_keyboard)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


def __delete_activity_before_vote(chat_id: str, message_id: int, activity_name: str):
    try:
        vote_keyboard = markup.create_activity_voter_markup("delete", activity_name)
        bot.delete_message(chat_id=chat_id, message_id=message_id)
        bot.send_message(chat_id=chat_id, text=msg.DELETE_ACTIVITY_2.format(activity_name), reply_markup=vote_keyboard)
    except Exception as e:
        print(e)
        bot.send_message(chat_id, msg.ERROR_BASIC)


def __delete_activity_after_vote(chat_id: str, message_id: int, username: str, activity_name: str, vote: str):
    try:
        bot.delete_message(chat_id, message_id)
        if vote == "Yes":
            activities.delete(username, activity_name)
            bot.send_message(chat_id, msg.DELETE_ACTIVITY_3_1.format(activity_name))
        else:
            bot.send_message(chat_id, msg.DELETE_ACTIVITY_4_1.format(activity_name))
    except Exception as e:
        print(e)
        bot.send_message(chat_id, msg.ERROR_BASIC)


@bot.message_handler(commands=['activities'])
def activities_(message):
    print(f"Message '{message.text}' from @{message.chat.username} in chat({message.chat.id})")
    try:
        str_list = "\n- " + "\n- ".join(activities.show_all_titles(message.chat.username))
        all_activities_msg = msg.ALL_ACTIVITIES.format(str_list)

        bot.send_message(message.chat.id, all_activities_msg)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


######################
#       TRACK        #
######################

@bot.message_handler(commands=['track'])
def track(message):
    print(f"Message '{message.text}' from @{message.chat.username} in chat({message.chat.id})")
    try:
        all_user_activity_titles = activities.show_all_titles(message.chat.username)
        activities_keyboard = markup.create_inline_markup('track', all_user_activity_titles)

        bot.send_message(message.chat.id, msg.TRACK_1, reply_markup=activities_keyboard)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


def __track_post_activity_answer(chat_id: str, message_id: int, activity_name: str):
    try:
        bot.delete_message(chat_id, message_id)
        bot.send_message(chat_id, msg.TRACK_2.format(activity_name))
        bot.register_next_step_handler_by_chat_id(chat_id, __track_post_time_answer, activity_name)
    except Exception as e:
        print(e)
        bot.send_message(chat_id, msg.ERROR_BASIC)


def __track_post_time_answer(message, activity: str):
    # todo: validate time
    try:
        hours_and_minutes_str: str = message.text
        hours, minutes = time.extract_hours_and_minutes(hours_and_minutes_str)

        end_time = time.now()
        start_time = time.minus(end_time, hours=hours, minutes=minutes)

        e_start = events.create(
            username=message.chat.username,
            activity_name=activity,
            event_type=EventType.START,
            time=start_time)

        events.create(
            username=message.chat.username,
            activity_name=activity,
            event_type=EventType.STOP,
            time=end_time,
            last=e_start.id)

        bot.send_message(message.chat.id, msg.FINISHED_TRACKING.format(activity, hours, minutes))
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


@bot.message_handler(commands=['start_tracking'])
def start_tracking(message):
    print(f"Message '{message.text}' from @{message.chat.username} in chat({message.chat.id})")
    try:
        started_titles = activities.all_started_activity_titles(message.chat.username)
        all_user_activity_titles = [a for a in activities.show_all_titles(message.chat.username) if
                                    a not in started_titles]

        activities_keyboard = markup.create_inline_markup('start_tracking', all_user_activity_titles)

        bot.send_message(message.chat.id, msg.START_TRACKING_1, reply_markup=activities_keyboard)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


def __start_tracking_post_answer(chat_id: str, activity: str, username: str, message_id: int):
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)

        events.create(username, activity, EventType.START)
        bot.send_message(chat_id, msg.START_TRACKING_2.format(activity))
    except Exception as e:
        print(e)
        bot.send_message(chat_id, msg.ERROR_BASIC)


@bot.message_handler(commands=['stop_tracking'])
def start_tracking(message):
    print(f"Message '{message.text}' from @{message.chat.username} in chat({message.chat.id})")
    try:
        started_activities = activities.all_started_activity_titles(message.chat.username)
        if len(started_activities) == 1:
            __stop_tracking_post_answer(chat_id=message.chat.id, activity=started_activities[0],
                                        username=message.chat.username)
        elif len(started_activities) > 1:
            activities_keyboard = markup.create_inline_markup('stop_tracking', started_activities)
            bot.send_message(message.chat.id, msg.STOP_TRACKING_2_1, reply_markup=activities_keyboard)
        else:
            bot.send_message(message.chat.id, msg.STOP_TRACKING_3_1)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


def __stop_tracking_post_answer(chat_id: str, activity: str, username: str, message_id: int = None):
    try:
        if message_id:
            bot.delete_message(chat_id=chat_id, message_id=message_id)

        print(f'Stop tracking activity({activity}) for user({username})')

        e_start = events.find_last(username, activity, EventType.START)
        e_stop = events.create(username=username, activity_name=activity, event_type=EventType.STOP, last=e_start.id)

        hours, minutes = time.count_difference(e_start.time, e_stop.time)

        bot.send_message(chat_id, msg.STOP_TRACKING_2_2.format(activity, hours, minutes))
    except Exception as e:
        print(e)
        bot.send_message(chat_id, msg.ERROR_BASIC)


######################
#       EVENT        #
######################

@bot.message_handler(commands=['show_last'])
def show_last(message):
    print(f"Message '{message.text}' from @{message.chat.username} in chat({message.chat.id})")
    try:
        bot.send_message(message.chat.id, msg.SHOW_LAST_1)
        bot.register_next_step_handler_by_chat_id(message.chat.id, __show_last_post_answer)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


def __show_last_post_answer(message):
    try:
        username = message.chat.username
        answ: str = message.text

        last_events_statistics: str = statistics_service.last_events_statistics(username, answ)
        bot.send_message(message.chat.id, msg.SHOW_LAST_2.format(answ, last_events_statistics))
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


@bot.message_handler(commands=['delete_last'])
def delete_last_tracking(message):
    print(f"Message '{message.text}' from @{message.chat.username} in chat({message.chat.id})")
    try:

        activities_keyboard = markup.create_inline_markup('delete_event',
                                                          activities.show_all_titles(message.chat.username))

        bot.send_message(message.chat.id, msg.DELETE_LAST_EVENT_1, reply_markup=activities_keyboard)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


def __delete_last_tracking_before_vote(chat_id: str, message_id: int, username: str, activity_name: str):
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)

        stop_event, start_event, statistics = events.find_last_events_pair(username, activity_name)
        statistics_data = statistics.to_str(with_counter=False)

        vote_keyboard = markup.create_activity_voter_markup('delete_event', data=activity_name)
        bot.send_message(chat_id=chat_id, text=msg.DELETE_LAST_EVENT_2.format(statistics_data),
                         reply_markup=vote_keyboard)
    except Exception as e:
        print(e)
        bot.send_message(chat_id, msg.ERROR_BASIC)


def __delete_last_tracking_after_vote(chat_id: str, message_id: int, vote: str, username: str, activity_name: str):
    try:
        bot.delete_message(chat_id, message_id)

        if vote == "Yes":
            stop_event, start_event, statistics = events.find_last_events_pair(username, activity_name)
            events.delete(stop_event.id, start_event.id)
            bot.send_message(chat_id, msg.DELETE_LAST_EVENT_3_1.format(statistics.to_str(with_counter=False)))
        else:
            bot.send_message(chat_id, msg.DELETE_LAST_EVENT_4_1)
    except Exception as e:
        print(e)
        bot.send_message(chat_id, msg.ERROR_BASIC)


@bot.message_handler(commands=['clear'])
def clear(message):
    print(f"Message '{message.text}' from @{message.chat.username} in chat({message.chat.id})")
    try:
        vote_keyboard = markup.create_voter_inline_markup("clear")
        bot.send_message(chat_id=message.chat.id, text=msg.CLEAR_1, reply_markup=vote_keyboard)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


def __clear_after_vote(chat_id: str, message_id: int, username: str, vote: str):
    try:
        bot.delete_message(chat_id, message_id)
        if vote == "Yes":
            events.delete_all(username)
            bot.send_message(chat_id, msg.CLEAR_2_1)
        else:
            bot.send_message(chat_id, msg.CLEAR_2_2)
    except Exception as e:
        print(e)
        bot.send_message(chat_id, msg.ERROR_BASIC)


#######################
#       REPORT        #
#######################

@bot.message_handler(commands=['statistics'])
def statistics(message):
    print(f"Message '{message.text}' from @{message.chat.username} in chat({message.chat.id})")

    try:
        bot.send_message(chat_id=message.chat.id, text=msg.STATISTIC_1)
        bot.register_next_step_handler_by_chat_id(message.chat.id, __statistic_post_answer)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


def __statistic_post_answer(message):
    date_range_inp: str = message.text

    try:
        report_message: str = statistics_service.generate(message.chat.username, date_range_inp).to_str()
        bot.send_message(message.chat.id, report_message)
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, msg.ERROR_BASIC)


##############################
#       APP LAUNCHING        #
##############################

bot.polling(none_stop=True)

# @server.route('/' + config.BOT_API_KEY, methods=['POST'])
# def get_message():
#     json_string = request.get_data().decode('utf-8')
#     update = telebot.types.Update.de_json(json_string)
#     bot.process_new_updates([update])
#     return "!", 200
#
#
# @server.route("/")
# def webhook():
#     bot.remove_webhook()
#     bot.set_webhook(url='https://ltt-tg-bot.herokuapp.com/' + config.BOT_API_KEY)
#     return "!", 200
#
#
# if __name__ == "__main__":
#     server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
