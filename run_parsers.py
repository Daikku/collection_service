import codecs
import os
import sys
import django

project_path = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django.setup()

from collecting.parsers import *
from collecting.models import Vacancy, City, Language


parsers = (
    (parse_hhru, 'https://hh.ru/search/vacancy?text=Python&area=1'),
    (parse_rabotaru, 'https://www.rabota.ru/?query=python&sort=relevance&all_regions=1'),
)

works, errors = list(), list()
city = City.objects.filter(slug='moskva')

for function, url in parsers:
    w, err = function(url)
    works.append(w)
    errors.append(err)

with codecs.open('work.txt', 'w', 'utf-8') as file:
    file.write(str(works))
