from django.shortcuts import render

from .forms import CollectionForm
from .models import Vacancy


def home_page(request):
    form = CollectionForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    vacancies = list()
    if city or language:
        _filter = dict()
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        vacancies = Vacancy.objects.filter(**_filter)
    return render(request, 'collecting/home_page.html', {'vacancies': vacancies, 'form': form})
