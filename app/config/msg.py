ACTIVITIES_COMMAND = "activities"
ADD_ACTIVITY_COMMAND = "add\_activity"
DELETE_ACTIVITY_COMMAND = "delete\_activity"

TRACK_COMMAND = "track"
START_COMMAND = "start\_tracking"
STOP_COMMAND = "stop\_tracking"

LAST_EVENTS_COMMAND = "last\_events"

STATISTICS_COMMAND = "statistics"

START = f"""
Hi 👋! I'm @LifeTimeTrackerBot

With me, you will know how really you spend your life.
📊 Let's analyze your time!

Commands:

/{ACTIVITIES_COMMAND} - show all activities
/{ADD_ACTIVITY_COMMAND} - create a new activity
/{DELETE_ACTIVITY_COMMAND} - delete your activity

/{TRACK_COMMAND} - create a new  finished event for your activity
/{START_COMMAND} - start a new event for your activity
/{STOP_COMMAND} - stop the started event

/{LAST_EVENTS_COMMAND} - show last `n` events for activity

/{STATISTICS_COMMAND} - show statistics for the chosen time range
"""
# /distracted - to write distracted time for your event.sql

# universal

CHOOSE_ACTIVITY = """🪄 Please choose an activity:"""

# /activities

ALL_ACTIVITIES = "📋 All your activities: {} \n\n/" + ADD_ACTIVITY_COMMAND + " - ➕ add activity \n/" + DELETE_ACTIVITY_COMMAND + " - ➖ delete activity "

# /add_activity

ADD_ACTIVITY_1 = """✍️ Write the name for a new activity: """
ADD_ACTIVITY_2 = "Created new activity with the name `{}`. \n\n/" + ACTIVITIES_COMMAND + " - 👁 see all your activities"

# /delete_activity

DELETE_ACTIVITY_1 = CHOOSE_ACTIVITY
DELETE_ACTIVITY_2 = """🗑 Do you want to delete the activity `{}`?"""
DELETE_ACTIVITY_3_1 = "✅ Deleted activity with the name `{}`. \n\n/" + ACTIVITIES_COMMAND + " - 👁 see all your activities"
DELETE_ACTIVITY_4_1 = "❌ Deletion is canceled. \n\n/" + ACTIVITIES_COMMAND + " - 👁 see all your activities"

# /track

TRACK_1 = CHOOSE_ACTIVITY
TRACK_2 = """`{}` 🕔 How long? \nExamples: `1h20m`, `10m`, `3h`"""
FINISHED_TRACKING = """✅ Tracked `{}`. Totally spent {} hours {} minutes. Good Job 👍"""

# /start_tracking

START_TRACKING_1 = CHOOSE_ACTIVITY
START_TRACKING_2 = "Started ✔️️ Please, don't forget to send /" + STOP_COMMAND + " after you finish the `{}`. Have fun!"

# /stop_tracking

STOP_TRACKING_1 = FINISHED_TRACKING
STOP_TRACKING_2_1 = CHOOSE_ACTIVITY
STOP_TRACKING_2_2 = FINISHED_TRACKING
STOP_TRACKING_3_1 = f""" Oh, I can't stop nothing 🤷‍. Please start 🆕 activity by /{START_COMMAND}, or track already finished 🏁 activity with /{TRACK_COMMAND} command."""

# /last_events

LAST_EVENTS_1 = "✍️ Write a number of how many last events you want to see. 🔝 Max number: `20`."
LAST_EVENTS_2 = "🔎 Your last `{}` events:\n{}"

LAST_EVENTS_LIST_PREFIX = "➡️ "

# /delete_event

DELETE_EVENT_1 = CHOOSE_ACTIVITY
DELETE_EVENT_2_1 = "🗳 Please, choose one `{}` event that you want to delete:"
DELETE_EVENT_2_2 = "🤷 Can't find any events for the activity `{}`"
DELETE_EVENT_3 = "🗑 Do you want to delete this event?"
DELETE_EVENT_4_1 = "✅ Event deleted."
DELETE_EVENT_5_1 = "❌ Deletion is canceled."

# /statistics

STATISTIC_1 = "📆 Please write period \nExamples: `1D`, `1W`, `1M` for last time range, or `01.01.2021 - 05.01.2021`"
STATISTIC_2 = '📊 Full Report for ({} - {}) \n\n{}'

# ERRORS

ERROR_BASIC = "🙈 Sorry, something went wrong. Please try again..."

# VOTE

YES = '✅ Yes'
NO = '❌ No'
