from telebot import types


def empty_markup():
    return types.InlineKeyboardMarkup()


def create_activity_voter_markup(event_name: str, data: str, title: str = "payload"):
    return create_voter_inline_markup(event_name, (title, data))


def create_voter_inline_markup(vote_prefix: str, *additional):
    return create_inline_markup(vote_prefix + "_vote", ["Yes", "No"], *additional)


def create_inline_markup(key, button_names, *additional):
    activities_keyboard = types.InlineKeyboardMarkup()

    additional_json: str = ',' + ','.join([f'"{a[0]}": "{a[1]}"' for a in additional]) if additional else ''

    for b_name in button_names:
        activities_keyboard.add(types.InlineKeyboardButton(
            text=b_name,
            callback_data='{"' + key + '": "' + b_name + '" ' + additional_json + '}')
        )

    return activities_keyboard


def create_reply_markup(button_names):
    activities_keyboard = types.ReplyKeyboardMarkup()

    for name in button_names:
        activities_keyboard.add(types.KeyboardButton(text=name))

    return activities_keyboard
