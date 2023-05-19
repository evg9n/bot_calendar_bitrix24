from loader import bot
import fast_bitrix24
from datetime import datetime as dt
from re import match
from utils.work_data import get_json, set_json


def datetime_now() -> str:
    """
    Определяет текущую дату и время без миллисекунд, возвращает str
    """
    pattern = r"(\d{4}-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}))"
    now = str(dt.now())
    now = match(pattern=pattern, string=now)
    return now.group()


def get_data_meet(hook: str, meet_id: int, active: bool) -> str:
    bx24 = fast_bitrix24.Bitrix(hook)
    affairs = bx24.get_all(method='calendar.event.getbyid',
                           params={'id': meet_id})
    name = affairs["NAME"]
    date_from = f'Занято с {affairs["DATE_FROM"][:-3]}({affairs["TZ_FROM"]})'
    date_to = f'До {affairs["DATE_TO"][:-3]}({affairs["TZ_TO"]})'
    discription = affairs["DESCRIPTION"]

    message = f"""
❗{"Новая встреча" if active else "Отмена встречи"}❗
{name}
{discription}
{date_from}
{date_to}
"""

    return message


def get_affairs(hook: str, owner_id: int, now: str, chat_id, user_id):
    bx24 = fast_bitrix24.Bitrix(hook)
    affairs = bx24.get_all(method='calendar.event.get',
                           params={'type': 'user',
                                   'ownerId': owner_id,
                                   'from': now})
    data = get_json(user_id=user_id)
    list_id = data['list_id']

    for e in affairs:
        meet_id = e['ID']
        if e['MEETING_STATUS'] == 'Y':
            if meet_id not in list_id:
                message = get_data_meet(hook=hook, meet_id=meet_id, active=True)
                bot.send_message(user_id, text=message)
                list_id.append(meet_id)

        elif e['MEETING_STATUS'] == 'N':
            if meet_id in list_id:
                message = get_data_meet(hook=hook, meet_id=meet_id, active=False)
                bot.send_message(user_id, text=message)
                list_id.remove(meet_id)

    # data['list_id'] = list_id
    set_json(data, user_id)
    # return list_id

