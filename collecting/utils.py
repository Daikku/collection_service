from uuid import uuid4
from pytils.translit import slugify


def unique_slugify(instance, slug):
    """
    Создание уникального slug при повторении
    """
    model = instance.__class__
    unique_slug = slugify(slug)
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{uuid4().hex[:8]}'
    return unique_slug


def default_urls_data():
    """
    Задать данные по умолчанию для url запроса
    """
    return {'parse_hhru': '', 'parse_rabotaru': ''}

