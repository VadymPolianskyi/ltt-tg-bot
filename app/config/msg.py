ACTIVITIES_COMMAND = "activities"
ADD_ACTIVITY_COMMAND = "add\_activity"
DELETE_ACTIVITY_COMMAND = "delete\_activity"

TRACK_COMMAND = "track"
START_COMMAND = "start"
STOP_COMMAND = "stop"

CLEAR_COMMAND = "clear"

STATISTICS_COMMAND = "statistics"

START = f"""
Hi! I'm the @LifeTimeTrackerBot

With me you will know how really you spend your life.
I work with the next commands:

/{ACTIVITIES_COMMAND} - show all activities
/{ADD_ACTIVITY_COMMAND} - create a new activity
/{DELETE_ACTIVITY_COMMAND} - delete your activity

/{TRACK_COMMAND} - create a new  finished event for your activity
/{START_COMMAND} - start a new event for your activity
/{STOP_COMMAND} - stop the started event

/{CLEAR_COMMAND} - clear all events for all activities

/{STATISTICS_COMMAND} - show statistics for the chosen time range
"""
# /distracted - to write distracted time for your event.sql
# /last_tracking - shows last 10 events

# universal

CHOOSE_ACTIVITY = """Please choose activity:"""

# /activities

ALL_ACTIVITIES = "All your activities: {} \n\n/" + ADD_ACTIVITY_COMMAND + " - add activity\n/" + DELETE_ACTIVITY_COMMAND + " - delete activity"

# /add_activity

ADD_ACTIVITY_1 = """Please write the name for a new activity"""
ADD_ACTIVITY_2 = "Created new activity with name `{}`. Write /" + ACTIVITIES_COMMAND + " to see all your activities."

# /delete_activity

DELETE_ACTIVITY_1 = CHOOSE_ACTIVITY
DELETE_ACTIVITY_2 = """Are you sure that you want to delete the activity `{}`?"""
DELETE_ACTIVITY_3_1 = "Deleted activity with name `{}`. Write /" + ACTIVITIES_COMMAND + " to see all your activities."
DELETE_ACTIVITY_4_1 = "Deletion for activity `{}` is canceled. Write /" + ACTIVITIES_COMMAND + " to see all your activities."

# /track

TRACK_1 = CHOOSE_ACTIVITY
TRACK_2 = """Got you. `{}`. How long?"""
FINISHED_TRACKING = """Tracked `{}`. Totally spent {} hours {} minutes."""

# /start

START_TRACKING_1 = CHOOSE_ACTIVITY
START_TRACKING_2 = "Started! Please, don't forget to send /" + STOP_COMMAND + " after you finish `{}`. Have fun!"

# /stop

STOP_TRACKING_1 = FINISHED_TRACKING
STOP_TRACKING_2_1 = CHOOSE_ACTIVITY
STOP_TRACKING_2_2 = FINISHED_TRACKING
STOP_TRACKING_3_1 = f""" Oh, I can't stop NOTHING. Please start activity by /{START_COMMAND}, or track already finished activity with /{TRACK_COMMAND} command."""

# /statistics

STATISTIC_1 = "Please write period \n Example: `1D`, `1W`, `1M` for last time range, or `01.01.2021 - 05.01.2021`"
STATISTIC_2 = "That's how was your {}"

# /clear

CLEAR_1 = "Do you want to clear all your events for all your activities?"
CLEAR_2_1 = "Done! Now your history is clear."
CLEAR_2_2 = "Clearing is canceled. Continue using me :)"

# ERRORS

ERROR_BASIC = "Sorry, something went wrong. Please try again..."
