import codecs
import os
import sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

project_path = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()


from collecting.parsers import *
from collecting.models import Vacancy, City, Language, Error, Url


parsers = (
    (parse_hhru, 'https://hh.ru/search/vacancy?text=Python&area=1'),
    (parse_rabotaru, 'https://www.rabota.ru/?query=python&sort=relevance&all_regions=1'),
)

User = get_user_model()


def get_values_user():
    """
    Получение значений города и ЯП по введённой пользователем информации
    """
    queryset = User.objects.all().values()
    values_user = set((query['city_id'], query['language_id']) for query in queryset)
    return values_user


def get_urls(values: set):
    """
    Получение url адреса и его параметров в соответствии с городом и ЯП
    """
    queryset = Url.objects.all().values()
    urls_dict = {(query['city_id'], query['language_id']): query['url_param'] for query in queryset}
    urls = list()
    for value in values:
        data = dict()
        data['city'] = value[0]
        data['language'] = value[1]
        data['url_param'] = urls_dict[value]
        urls.append(data)
    return urls


works, errors = list(), list()

queryset_user = get_values_user()
urls = get_urls(queryset_user)

city = City.objects.filter(slug='moskva').first()
language = Language.objects.filter(slug='python').first()

for function, url in parsers:
    w, err = function(url)
    works += w
    errors += err

for work in works:
    vac = Vacancy(**work, city=city, language=language)
    try:
        vac.save()
    except DatabaseError:
        print('ОШИБКА!!! Данные не сохранены в базе.')

if errors:
    error = Error(errors).save()

# with codecs.open('work.txt', 'w', 'utf-8') as file:
# file.write(str(works))
