import requests
from bs4 import BeautifulSoup as bs
import codecs
from random import randint

__all__ = ('parse_hhru', 'parse_rabotaru')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'},
    {'User-Agent': '"Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/532.9 (KHTML, like Gecko) \
        Chrome/5.0.307.11 Safari/532.9"',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-in; HTC_DesireS_S510e Build/GRJ90) \
        AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'},
    ]

def parse_hhru(url: str):
    works = list()
    errors = list()
    response = requests.get(url, headers=headers[randint(0, 2)])
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        main_div = soup.find('div', id='a11y-main-content')
        if main_div:
            items_div = main_div.find_all('div', attrs={'class': 'vacancy-serp-item__layout'})
            for item in items_div:
                title = item.find('h3')
                url_vacancy = title.a['href']
                company_div = item.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'})
                company = company_div.a.text
                city = item.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
                works.append({'title': title.text, 'url': url_vacancy, "company": company, 'city': city})
        else:
            errors.append({'url': url, 'title': 'ERROR: Div not found'})
    else:
        errors.append({'url': url, 'title': 'ERROR: Page do not response'})

    return works, errors

def parse_rabotaru(url: str):
    works = list()
    errors = list()
    domain = 'https://www.rabota.ru/'
    response = requests.get(url, headers=headers[randint(0, 2)])
    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        main_div = soup.find('div', attrs={'class': 'home-vacancies__infinity-list'})
        if main_div:
            items_div = main_div.find_all('div', attrs={'class': 'vacancy-preview-card__top'})
            for item in items_div:
                title = item.find('h3')
                url_vacancy = title.a['href']
                description = item.find('div', attrs={'itemprop': 'description'}).text
                company_div = item.find('span', attrs={'class': 'vacancy-preview-card__company-name'})
                company = company_div.text
                city = item.find('span', attrs={'itemprop': 'address'}).text
                works.append({'title': title.text, 'url': domain + url_vacancy, 'description': description,
                              "company": company, 'city': city})
        else:
            errors.append({'url': url, 'title': 'ERROR: Div not found'})
    else:
        errors.append({'url': url, 'title': 'ERROR: Page do not response'})

    return works, errors