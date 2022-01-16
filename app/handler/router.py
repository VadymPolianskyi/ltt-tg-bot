import json

from telebot.types import CallbackQuery


class CallbackRouter:
    def __init__(self, callback_handlers: list):
        callback_handlers_dict = dict()
        for ch in callback_handlers:
            callback_handlers_dict[ch.MARKER] = ch

        self.callback_handler: dict = callback_handlers_dict

    def route(self, call: CallbackQuery):
        payload: dict = json.loads(call.data)

        for key in payload.keys():
            if key in self.callback_handler:
                print(f"Found route for callback '{key}' from user({call.from_user.id})")
                self.callback_handler[key].handle(call)
                break
