from queue import Queue
from time import sleep
from utils.check_bitrix24 import datetime_now, get_affairs
from random import randint
from aiohttp.client_exceptions import ClientResponseError
from loader import bot
from keyboards.reply import menu


data_queue = Queue()
monitoring = dict()


def check_updates(**kwargs):
    while monitoring.get(kwargs.get('user_id')):
        if kwargs.get('hook'):
            hook = kwargs.get('hook')
            owner_id = kwargs.get('owner_id')
            user_id = kwargs.get('user_id')

            try:
                get_affairs(hook=hook, owner_id=owner_id, user_id=user_id)
            except ClientResponseError:
                bot.send_message(chat_id=user_id,
                                 text='Некорректный webhook обратитесь к справке через /help',
                                 reply_markup=menu())
                monitoring[kwargs.get('user_id')] = False
        else:
            monitoring[kwargs.get('user_id')] = False

        sleep(randint(10, 60))
