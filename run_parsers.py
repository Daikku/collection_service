import codecs
import os
import sys
from django.db import DatabaseError

project_path = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django

django.setup()

from collecting.parsers import *
from collecting.models import Vacancy, City, Language, Error

parsers = (
    (parse_hhru, 'https://hh.ru/search/vacancy?text=Python&area=1'),
    (parse_rabotaru, 'https://www.rabota.ru/?query=python&sort=relevance&all_regions=1'),
)

works, errors = list(), list()
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
