from loader import bot
from telebot.types import Message
from keyboards.reply import menu_button, menu, close
from state import StateCheck
from utils.work_data import get_json, set_json
from re import findall


@bot.message_handler(func=lambda message: message.text == menu_button[1] or message.text == '/install')
def install(message: Message):
    bot.set_state(user_id=message.from_user.id,
                  state=StateCheck.state_webhook,
                  chat_id=message.chat.id)
    bot.send_message(chat_id=message.from_user.id, text='Пришли webhook', reply_markup=close())


@bot.message_handler(state=StateCheck.state_webhook)
def install_webhook(message: Message):
    text = message.text
    user_id = findall(r'\/(\d+)\/', text)
    if (text.count('/') == 5 or text.count('/')) == 6 \
            and text.startswith('https://') \
            and 'bitrix24.ru' in text and user_id != []:
        data = get_json(user_id=message.from_user.id)
        data['webhook'] = text
        data['user_id'] = user_id[0]
        set_json(data=data, user_id=message.from_user.id)

        bot.set_state(user_id=message.from_user.id,
                      state=None,
                      chat_id=message.chat.id)
        bot.send_message(chat_id=message.from_user.id, text='Готово', reply_markup=menu())
    else:
        bot.send_message(chat_id=message.from_user.id,
                         text='Некорректный webhook\nПрочитай инструкцию /help и пришли заново')


@bot.message_handler(state=StateCheck.state_user_id)
def install_user_id(message: Message):
    data = get_json(user_id=message.from_user.id)
    data['uesr_id'] = message.text
    set_json(data=data, user_id=message.from_user.id)

    bot.set_state(user_id=message.from_user.id,
                  state=None,
                  chat_id=message.chat.id)
    bot.send_message(chat_id=message.from_user.id, text='Готово', reply_markup=menu())
