from telebot.handler_backends import State, StatesGroup


class StateCheck(StatesGroup):
    state_webhook = State()
    state_user_id = State()
    state_track = State()
