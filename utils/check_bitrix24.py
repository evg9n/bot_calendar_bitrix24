import re

from loader import bot
import fast_bitrix24
from datetime import datetime as dt, timedelta, datetime
from re import match
from utils.work_data import get_json, set_json


def check_date(date: str):
    # "30.05.2023 14:35(Europe/Moscow)"

    pattern_date = r"\d{2}.\d{2}.\d{4}"
    pattern_time = r"\d{2}:\d{2}"
    result_date = re.search(pattern_date, date)
    result_time = re.search(pattern_time, date)

    if result_date and result_time:
        result_date = result_date.group()
        result_time = result_time.group()

        day, month, year = str(result_date).split('.')
        hour, minute = str(result_time).split(':')

        res = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute))
        now = datetime.now()

        if res > now:
            return False

    return True


def create_message(info_meet, active) -> str:
    name = info_meet["name"]
    date_from = f'Занято с {info_meet["date_from"]}({info_meet["tz_from"]})'
    date_to = f'До {info_meet["date_to"]}({info_meet["tz_to"]})'
    discription = info_meet["discription"]
    message = f"""
    ❗{"Новая встреча" if active else "Отмена встречи"}❗
    {name}
    {discription}
    {date_from}
    {date_to}
    """
    return message


def datetime_now() -> str:
    """
    Определяет текущую дату и время без миллисекунд, возвращает str
    """
    pattern = r"(\d{4}-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}))"
    now = str(dt.now() - timedelta(hours=3))
    now = match(pattern=pattern, string=now)
    if now:
        return now.group()
    else:
        # todo изменить
        return ''


def datetime_future(days: int):
    """
    Определяет будущую дату и время без миллисекунд, возвращает str
    """
    pattern = r"(\d{4}-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}))"
    date = str(dt.now() + timedelta(days=days))
    date = match(pattern=pattern, string=date)
    if date:
        return date.group()
    else:
        # todo изменить
        return ''


def get_data_meet(hook: str, meet_id: int) -> dict:
    bx24 = fast_bitrix24.Bitrix(hook)
    affairs = bx24.get_all(method='calendar.event.getbyid',
                           params={'id': meet_id},
                           )
    info_meet = dict(
        name=affairs["NAME"],
        date_from=affairs["DATE_FROM"][:-3],
        tz_from=affairs["TZ_FROM"],
        date_to=affairs["DATE_TO"][:-3],
        tz_to=affairs["TZ_TO"],
        discription=affairs["DESCRIPTION"]
    )
    return info_meet


def get_affairs(hook: str, owner_id: int, user_id) -> None:
    data = get_json(user_id=user_id)
    now = datetime_now()
    days = int(data.get('days'))
    future = datetime_future(days=days)
    bx24 = fast_bitrix24.Bitrix(hook)
    affairs = bx24.get_all(method='calendar.event.get',
                           params={'type': 'user',
                                   'ownerId': owner_id,
                                   'from': now,
                                   'to': future})
    list_id = list(data['list_id'].keys())
    result_meet_id = list()

    for e in affairs:
        meet_id = e['ID']
        result_meet_id.append(meet_id)

        if e['MEETING_STATUS'] == 'Y':
            if meet_id not in list_id:
                info_meet = get_data_meet(hook=hook, meet_id=meet_id)
                message = create_message(info_meet=info_meet, active=True)
                bot.send_message(user_id, text=message)
                data['list_id'][meet_id] = info_meet

        elif e['MEETING_STATUS'] == 'N':
            if meet_id in list_id:
                info_meet = get_data_meet(hook=hook, meet_id=meet_id)
                message = create_message(info_meet=info_meet, active=False)
                bot.send_message(user_id, text=message)
                data['list_id'].pop(meet_id)

    list_id = list(data['list_id'].keys())

    for meet_id in list_id:
        if meet_id not in result_meet_id:

            if meet_id in list_id:
                date = data['list_id'][meet_id]['date_from']

                if check_date(date=date):
                    data['list_id'].pop(meet_id)
                else:
                    info_meet = data['list_id'][meet_id]
                    message = create_message(info_meet=info_meet, active=False)
                    bot.send_message(chat_id=user_id, text=message)
                    data['list_id'].pop(meet_id)

    set_json(data, user_id)

