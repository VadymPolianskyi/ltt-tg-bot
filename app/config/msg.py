TIME_ZONE_COMMAND = "time\_zone"

CATEGORIES_COMMAND = "categories"
ADD_CATEGORY_COMMAND = "add\_category"
DELETE_CATEGORY_COMMAND = "delete\_category"

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

/{TIME_ZONE_COMMAND} - manage your time zone (`UTC` by default)

/{ACTIVITIES_COMMAND} - show all activities
/{ADD_ACTIVITY_COMMAND} - create a new activity
/{DELETE_ACTIVITY_COMMAND} - delete your activity

/{TRACK_COMMAND} - create a new  finished event for your activity
/{START_COMMAND} - start a new event for your activity
/{STOP_COMMAND} - stop the started event

/{LAST_EVENTS_COMMAND} - show last `n` events for activity

/{STATISTICS_COMMAND} - show statistics for the chosen time range
"""

MENU = """
With me, you will know how really you spend your life 🚀
Let's analyze your time!

🪄 Choose:
"""
# /distracted - to write distracted time for your event.sql


# BUTTONS
CATEGORIES_BUTTON = '📂 Categories'

ADD_CATEGORY_BUTTON = "➕ Add Category"
ADD_ACTIVITY_BUTTON = "➕ Add Activity"

SETTINGS_BUTTON = "⚙️ Settings"
EDIT_NAME_BUTTON = "✏️ Edit name"
DELETE_BUTTON = "🗑️ Delete"
CHANGE_CATEGORY_BUTTON = "📂 Change Category"

START_TRACKING_BUTTON = '▶️ Start Tracking'
STOP_TRACKING_BUTTON = '⏹ Stop Tracking'
TRACK_BUTTON = '⏱ Track'

STATISTICS_BUTTON = '📊 Statistics'

CHANGE_TIME_ZONE_BUTTON = '🌎 Change Time Zone'

BACK_BUTTON = '🔙 Back'

# universal

CHOOSE_ACTIVITY = """🪄 Please choose an activity:"""
CHOOSE_CATEGORY = """🪄 Please choose a category:"""

CATEGORY_SIGN = '📂'

# Category

ALL_CATEGORIES = '🗄 All your categories:'

ADD_CATEGORY = """✍️ Write the name for a new 📂 Category: """
ADD_CATEGORY_DONE = "Created new 📂 Category with the name `{}`."

CATEGORY = "📂 Category `{}`:"

EDIT_CATEGORY_NAME = "✍️ Write a new name for the 📂 Category `{}`:"
EDIT_CATEGORY_NAME_DONE = "Changed name 📂 `{}` ->  📂 `{}`."

ALL_CATEGORY_ACTIVITIES = "📂 Category `{}`:"

DELETE_CATEGORY = "🗑 Do you want to delete the 📂 Category `{}`?"
DELETE_CATEGORY_REGECT = "❌ You can't delete the category that contains activities. 🚮 Please clear all activities in 📂 Category `{}`."
DELETE_CATEGORY_DONE = "✅ Deleted 📂 Category `{}`."
DELETE_CATEGORY_CANCEL = "❌ Deletion is canceled."

# Activity

ADD_ACTIVITY = "✍️ Write the name for a new activity: "
ADD_ACTIVITY_DONE = "✅ Created new activity with the name `{}`"

ACTIVITY_SETTINGS = "Activity `{}` settings:"

EDIT_ACTIVITY_NAME = "✍️ Write a new name for the Activity `{}`:"
EDIT_ACTIVITY_NAME_DONE = "✅ Changed Activity name `{}` -> `{}`."

EDIT_ACTIVITY_CATEGORY = "🪄 Please choose a new 📂 Category for Activity `{}`:"
EDIT_ACTIVITY_CATEGORY_DONE = "✅ Moved Activity `{}` to 📂 Category `{}`."

DELETE_ACTIVITY_2 = "🗑 Do you want to delete the activity `{}`?"
DELETE_ACTIVITY_3_1 = "✅ Deleted Activity `{}`"
DELETE_ACTIVITY_4_1 = "❌ Deletion is canceled."

# /track

TRACK_1 = CHOOSE_CATEGORY
TRACK_2 = CHOOSE_ACTIVITY
TRACK_3 = """`{}` 🕔 How long? \nExamples: `1h20m`, `10m`, `3h`"""
FINISHED_TRACKING = """✅ Tracked `{}`. Totally spent {} hours {} minutes. Good Job 👍"""

# /start_tracking

START_TRACKING_1 = CHOOSE_CATEGORY
START_TRACKING_2 = CHOOSE_ACTIVITY
START_TRACKING_3 = "Started ✔️️"

# /stop_tracking

STOP_TRACKING_1 = FINISHED_TRACKING
STOP_TRACKING_2_1 = CHOOSE_ACTIVITY
STOP_TRACKING_2_2 = FINISHED_TRACKING
STOP_TRACKING_3_1 = f"Oh, I can't stop nothing 🤷‍. Please start 🆕 activity."

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

# /time_zone

TIMEZONE_BUTTON = "🌎 Change Time Zone"

TIMEZONE_1 = "🕐 Your current Time Zone is `{}`. ⌚️ Your current time is `{}`"
TIMEZONE_2 = "🌏 Please write your Time Zone in the format `Continent/City`. (MAKE SURE that you've finished all your events before changing Time Zone) \nP.S. 🙋 this [site](http://www.timezoneconverter.com/cgi-bin/findzone.tzc) can help you to find your time zone."
TIMEZONE_3 = "✅ Time Zone is changed on `{}`"

# /statistics

STATISTIC_1 = "📆 Please write period \nExamples: `1D`, `1W`, `1M` for last time range, or `01.01.2021 - 05.01.2021`"
STATISTIC_2 = '📊 Full Report for ({}) \n\n{}'

# ERRORS

ERROR_BASIC = "🙈 Sorry, something went wrong. Please try again..."

# VOTE

YES = '✅ Yes'
NO = '❌ No'
