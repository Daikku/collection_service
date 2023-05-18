from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import CollectionForm
from .models import Vacancy


def home_page(request):
    form = CollectionForm()
    return render(request, 'collecting/home_page.html', {'form': form})

def list_view(request):
    form = CollectionForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        _filter = dict()
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        vacancies = Vacancy.objects.filter(**_filter)

        paginator = Paginator(vacancies, 10)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context['vacancies'] = page_object
    return render(request, 'collecting/list_page.html', context=context)
