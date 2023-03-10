import codecs
from collecting.parsers import *

parsers = (
    (parse_hhru, 'https://hh.ru/search/vacancy?text=Python&area=1'),
    (parse_rabotaru, 'https://www.rabota.ru/?query=python&sort=relevance&all_regions=1'),
)

works, errors = list(), list()

for function, url in parsers:
    w, err = function(url)
    works.append(w)
    errors.append(err)

with codecs.open('work.txt', 'w', 'utf-8') as file:
    file.write(str(works))
