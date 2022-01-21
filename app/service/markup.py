from aiogram import types

from app.config import msg

VOTE_MARK = '_v'
EMPTY_VOTE_RESULT = '_'


def create_voter_inline_markup(vote_prefix: str, value: str):
    return create_inline_markup(vote_prefix + VOTE_MARK, [(msg.YES, value), (msg.NO, EMPTY_VOTE_RESULT)])


def create_simple_inline_markup(key, button_names: list):
    buttons = [(e, e) for e in button_names]
    return create_inline_markup(key, buttons)


def create_inline_markup(key, button_name_value_tuples: list):
    activities_keyboard = types.InlineKeyboardMarkup()

    for element in button_name_value_tuples:
        b_name = element[0]
        b_value = element[1]
        activities_keyboard.add(types.InlineKeyboardButton(
            text=b_name,
            callback_data='{"' + key + '": "' + b_value + '"}')
        )

    return activities_keyboard
