from django.contrib import admin

from collecting.models import City, Language, Vacancy, Error


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'city', 'language')
    list_display_links = ('id', 'title')
    list_filter = ('city__name', 'language__name')

@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    list_display = ('timestamp',)
    list_display_links = ('timestamp',)