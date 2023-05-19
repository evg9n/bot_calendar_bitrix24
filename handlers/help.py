from loader import bot
from telebot.types import Message
from os.path import join
from keyboards.reply import menu_button


@bot.message_handler(func=lambda message: message.text == menu_button[3] or message.text == '/help')
def help(message: Message):
    text = """
Кнопка "Следить":
запускает мониторинг вашего календаря из bitrix24, для мониторинга обязательно нужно указать webhook

Кнопка "Установить(Обновить) webhook":
После нажатия нужно будет прислать боту webhook, инструкция как его получить ниже
"""
    bot.send_message(chat_id=message.from_user.id, text=text)
    list_info = (

        'Нужно открыть веб-версию или декстоп версию bitrix24 и перейти в раздел "Разработчикам"',
        'В открывшемся окне выбрать "Другое"',
        'Далее выбрать "Входящий вебхук"',
        'Нужно в настройках прав указать "Календарь(calendar), '
        'потом сохранить ссылку на вебхук и нажать на кнопку сохранить\nПо всем вопросам обращаться к @jakegr99n',
    )
    for number in range(0, 4):
        path = join('screenshots', f'Screenshot_{number + 1}.png')
        with open(path, 'rb') as photo:
            bot.send_photo(chat_id=message.from_user.id, photo=photo, caption=f'{number + 1}. {list_info[number]}')

    text = """
Кнопка "Текущий webhook":
Показывает какой сейчас установлен webhook
"""
    bot.send_message(chat_id=message.from_user.id, text=text)
