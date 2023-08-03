from json import load, dump
from os.path import join, split
from os import listdir


def get_json(user_id) -> dict:
    """
    Получить данные из json файла
    """
    file = join('data', f"{user_id}.json")
    if split(file)[1] in listdir('data'):
        with open(file, 'r') as file:
            result = load(file)
        return result
    else:
        return dict(webhook='', days=14, user_id='', list_id={})


def set_json(data, user_id):
    """
    Записать данные в json файл
    """
    file_name = join('data', f"{user_id}.json")
    with open(file_name, 'w') as file:
        dump(data, file, ensure_ascii=False, indent=4)
