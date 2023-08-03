from json import dump
from os.path import join
from loader import bot
from telebot.types import Message
from keyboards.reply import menu, back_button, menu_button
from utils.check_updates import monitoring
from utils.work_data import get_json
from os import listdir


@bot.message_handler(commands=['start'])
def start(message: Message):

    file_name = join('data', f"{message.from_user.id}.json")

    if f"{message.from_user.id}.json" not in listdir('data'):
        user = dict(id=message.from_user.id,
                    is_bot=message.from_user.is_bot,
                    first_name=message.from_user.first_name,
                    username=message.from_user.username,
                    last_name=message.from_user.last_name,
                    language_code=message.from_user.language_code,
                    can_join_groups=message.from_user.can_join_groups,
                    can_read_all_group_messages=message.from_user.can_read_all_group_messages,
                    supports_inline_queries=message.from_user.supports_inline_queries,
                    is_premium=message.from_user.is_premium,
                    added_to_attachment_menu=message.from_user.added_to_attachment_menu)
        data = dict(webhook='', days=14, user_id='', user=user, list_id={})
        with open(file_name, 'w', encoding='utf-8') as file:
            dump(data, file, ensure_ascii=False, indent=4)

    text = "Привет!👋\nДля ознакомления жми /help 🗓"
    bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=menu())


@bot.message_handler(func=lambda message: message.text == back_button[0] or message.text == '/menu')
def start(message: Message):
    monitoring[message.from_user.id] = False
    bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
    bot.send_message(chat_id=message.from_user.id, text='Главное меню', reply_markup=menu())


@bot.message_handler(func=lambda message: message.text == menu_button[2] or message.text == 'current_hook')
def current_hook(message: Message):
    data = get_json(user_id=message.from_user.id)

    bot.send_message(
        chat_id=message.from_user.id,
        text=f'Текущий webhook: {data.get("webhook") if data.get("webhook") != "" else "не указан"}'
    )
