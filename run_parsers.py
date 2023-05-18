import os
import sys
import asyncio

from django.contrib.auth import get_user_model
from django.db import DatabaseError

project_path = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from collecting.parsers import *
from collecting.models import Vacancy, Error, Url

parsers = (
    (parse_hhru, 'parse_hhru'),
    (parse_rabotaru, 'parse_rabotaru'),
)

User = get_user_model()

works, errors = list(), list()


def get_values_user() -> set:
    """
    Получение значений города и ЯП по введённой пользователем информации
    """
    queryset = User.objects.all().values()
    values_user = set((query['city_id'], query['language_id']) for query in queryset)
    return values_user


def get_urls(values: set) -> list:
    """
    Получение url адреса и его параметров в соответствии с городом и ЯП
    """
    queryset = Url.objects.all().values()
    urls_dict = {(query['city_id'], query['language_id']): query['url_param'] for query in queryset}
    urls_lst = list()
    for value in values:
        data = dict()
        data['city'] = value[0]
        data['language'] = value[1]
        data['url_param'] = urls_dict[value]
        urls_lst.append(data)
    return urls_lst


queryset_user = get_values_user()
urls = get_urls(queryset_user)


async def main(value: tuple):
    """
    Асинхронная функция запуска парсеров сайтов по переданному кортежу, содержащему
    функцию, набор url, город и ЯП
    """
    function, url, city, language = value
    work, err = await loop.run_in_executor(None, function, url, city, language)
    errors.extend(err)
    works.extend(work)


loop = asyncio.get_event_loop()
lst_tasks = [(function, data['url_param'][key], data['city'], data['language'])
             for data in urls
             for function, key in parsers
             ]
tasks = asyncio.wait([loop.create_task(main(f)) for f in lst_tasks])

loop.run_until_complete(tasks)
loop.close()

for work in works:
    vac = Vacancy(**work)
    try:
        vac.save()
    except DatabaseError:
        print('ОШИБКА!!! Данные не сохранены в базе.')

if errors:
    error = Error(data=errors).save()
