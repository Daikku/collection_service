from django.db import models

from .utils import unique_slugify


class City(models.Model):
    name = models.CharField(verbose_name='Название города', max_length=30)
    slug = models.SlugField(verbose_name='Поле Slug', max_length=30, unique=True, blank=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class Language(models.Model):
    name = models.CharField(verbose_name='Язык программирования', max_length=20)
    slug = models.SlugField(verbose_name='Поле Slug', max_length=20, unique=True, blank=True)

    class Meta:
        verbose_name = 'Язык программирования'
        verbose_name_plural = 'Языки программирования'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)


class Vacancy(models.Model):
    url = models.URLField(verbose_name='Ссылка на вакансию')
    title = models.CharField(verbose_name='Название вакансии', max_length=150)
    company = models.CharField(verbose_name='Название компании', max_length=100)
    description = models.TextField(verbose_name='Описание вакансии')
    city = models.ForeignKey('City', verbose_name='Город', on_delete=models.CASCADE, related_name='vacancies')
    language = models.ForeignKey('Language', verbose_name='Язык программирования', on_delete=models.CASCADE,
                                 related_name='vacancies')
    time = models.DateTimeField(verbose_name='Время', auto_now_add=True)

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return f'{self.title}'


class Error(models.Model):
    timestamp = models.DateTimeField(verbose_name='Время ошибки', auto_now_add=True)
    data = models.JSONField(verbose_name='Содержание ошибки')

    class Meta:
        verbose_name = 'Ошибка'
        verbose_name_plural = 'Ошибки'

    def __str__(self):
        return f'Время ошибки: {self.timestamp}'