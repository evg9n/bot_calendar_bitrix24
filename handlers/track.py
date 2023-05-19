from loader import bot
from utils.check_updates import data_queue, check_updates
import threading
from telebot.types import Message
from keyboards.reply import menu_button, close
from utils.work_data import get_json
from utils.check_updates import monitoring
from state import StateCheck


@bot.message_handler(func=lambda message: message.text == menu_button[0] or message.text == '/track')
def track(message: Message):
    user_data = message.text
    data_queue.put(user_data)
    data = get_json(user_id=message.from_user.id)
    if data.get("webhook"):
        kwargs = {
            'hook': data['webhook'],
            'owner_id': data['user_id'],
            'user_id': message.from_user.id,
            'chat_id': message.chat.id,
        }
        monitoring[message.from_user.id] = True
        check_thread = threading.Thread(target=check_updates, kwargs=kwargs)
        check_thread.start()

        bot.set_state(user_id=message.from_user.id,
                      state=StateCheck.state_track,
                      chat_id=message.chat.id)
        bot.send_message(message.from_user.id, text="Отслеживание началось", reply_markup=close())
    else:
        bot.send_message(message.from_user.id, text="Webhook не установлен")
