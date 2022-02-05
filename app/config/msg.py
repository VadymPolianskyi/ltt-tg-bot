MENU = """
With me, you will know how really you spend your life 🚀
Let's analyze your time!
{}
🪄 Choose:
"""

# BUTTONS
CATEGORIES_BUTTON = '📂 Categories'

ADD_CATEGORY_BUTTON = "➕ Add Category"
ADD_ACTIVITY_BUTTON = "➕ Add Activity"

SETTINGS_BUTTON = "⚙️ Settings"
EDIT_NAME_BUTTON = "✏️ Edit name"
DELETE_BUTTON = "🗑️ Delete"
CHANGE_CATEGORY_BUTTON = "📂 Change Category"
LIST_EVENTS_BUTTON = "🔎 List events"

START_TRACKING_BUTTON = '▶️ Start Tracking'
STOP_TRACKING_BUTTON = '⏹ Stop Tracking'
TRACK_BUTTON = '⏱ Track'

STATISTICS_BUTTON = '📊 Statistics'

CHANGE_TIME_ZONE_BUTTON = '🌎 Change Time Zone'

NEXT_BUTTON = '➡️ Next'
BACK_BUTTON = '🔙 Back'

# PHRASES

CHOOSE_ACTIVITY = """🪄 Please choose an activity:"""
CHOOSE_CATEGORY = """🪄 Please choose a category:"""

CATEGORY_SIGN = '📂'
DELETE_SIGN = '❌'

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

DELETE_ACTIVITY_VOTE = "🗑 Do you want to delete the activity `{}`?"
DELETE_ACTIVITY_DONE = "✅ Deleted Activity `{}`"
DELETE_ACTIVITY_CANCELED = "❌ Deletion is canceled."

# Track

TRACK_CATEGORY = CHOOSE_CATEGORY
TRACK_ACTIVITY = CHOOSE_ACTIVITY
TRACK_TIME_RANGE = """`{}` 🕔 How long? \nExamples: `1h20m`, `10m`, `3h`"""
TRACK_FINISHED = """✅ Tracked `{}`. Totally spent {} hours {} minutes. Good Job 👍"""

START_TRACKING_CATEGORY = CHOOSE_CATEGORY
START_TRACKING_ACTIVITY = CHOOSE_ACTIVITY
START_TRACKING_DONE = "Started ✔️️"

STOP_TRACKING_DONE = TRACK_FINISHED
STOP_TRACKING_ACTIVITY = CHOOSE_ACTIVITY
STOP_TRACKING_NOTHING = f"Oh, I can't stop nothing 🤷‍. Please start 🆕 activity."

# Events

EVENT_LIST = "🗳 Events for Activity `{}`. Click on button if you want to ❌ delete event:"
DELETE_EVENT_VOTE = "🗑 Do you want to delete this event?"
DELETE_EVENT_DONE = "✅ Event deleted."
DELETE_EVENT_CANCELED = "❌ Deletion is canceled."

# User


TIMEZONE_CURRENT = "🕐 Your current Time Zone is `{}`. ⌚️ Your current time is `{}`"
TIMEZONE_EDIT = "🌏 Please write your Time Zone in the format `Continent/City`. (MAKE SURE that you've finished all your events before changing Time Zone) \nP.S. 🙋 this [site](http://www.timezoneconverter.com/cgi-bin/findzone.tzc) can help you to find your time zone."
TIMEZONE_DONE = "✅ Time Zone is changed on `{}`"

# /statistics
STATISTICS_CATEGORY_RESULT = CATEGORY_SIGN + ' `{}`:\n{}'


STATISTIC_PERIOD = "📆 Please write period \nExamples: `1D`, `1W`, `1M` for last time range, or `01.01.2021 - 05.01.2021`"
STATISTIC_RESULT = '📊 Full Report for ({}) \n\n{}'

# ERRORS

ERROR_BASIC = "🙈 Sorry, something went wrong. Please try again..."

# VOTE
YES = '✅ Yes'
NO = '❌ No'
