from django.shortcuts import render

from .models import Vacancy


def home_page(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'collecting/home_page.html', {'vacancies': vacancies})
