from loader import bot
from telebot.types import Message
from keyboards.reply import menu_button, menu, close
from state import StateCheck
from utils.work_data import get_json, set_json
from re import findall


@bot.message_handler(func=lambda message: message.text == menu_button[1] or message.text == '/install')
def install_webhook_handler(message: Message):
    bot.set_state(user_id=message.from_user.id,
                  state=StateCheck.state_webhook,
                  chat_id=message.chat.id)
    bot.send_message(chat_id=message.from_user.id, text='Пришли webhook', reply_markup=close())


@bot.message_handler(func=lambda message: message.text == menu_button[4])
def install_days_handler(message: Message):
    bot.set_state(user_id=message.from_user.id,
                  state=StateCheck.state_days,
                  chat_id=message.chat.id)
    info = get_json(user_id=message.from_user.id)
    text = (f'Сейчас установлено: {info.get("days")}'
            '\nНа сколько дней вперед смотреть?')
    bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=close())


@bot.message_handler(state=StateCheck.state_days)
def install_days(message: Message):
    text = message.text

    if text.isnumeric() and int(message.text) > 0:
        data = get_json(user_id=message.from_user.id)
        days = int(message.text)
        if days > 365:
            text = (f"{days} - Не многовато ли?🤔 Давай лучше попробуем к примеру там 30 дней"
                    "\nПришли еще раз пожалуйста)")
            bot.send_message(chat_id=message.from_user.id, text=text)
        else:
            data['days'] = days
            set_json(data=data, user_id=message.from_user.id)
            text = 'Установлено успешно'
            bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
            bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=menu())
    else:
        text = (f'{text} - странное определение количеству дней🤔'
                '\nДавай попробуем по-старинке, просто пришли мне пожалуйста положительное и целое число')
        bot.send_message(chat_id=message.from_user.id, text=text)


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

        bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
        bot.send_message(chat_id=message.from_user.id, text='Готово', reply_markup=menu())
    else:
        bot.send_message(chat_id=message.from_user.id,
                         text='Некорректный webhook\nПрочитай инструкцию /help и пришли заново')


@bot.message_handler(state=StateCheck.state_user_id)
def install_user_id(message: Message):
    data = get_json(user_id=message.from_user.id)
    data['uesr_id'] = message.text
    set_json(data=data, user_id=message.from_user.id)

    bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
    bot.send_message(chat_id=message.from_user.id, text='Готово', reply_markup=menu())
