from telebot.types import ReplyKeyboardMarkup, KeyboardButton


menu_button = ('Следить',
               "Установить(Обновить) webhook",
               "Текущий webhook",
               "Инструкция",)
back_button = ('Отмена',)


def menu() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = [KeyboardButton(text=text) for text in menu_button]
    return markup.add(*button)


def close() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button = [KeyboardButton(text=text) for text in back_button]
    return markup.add(*button)
