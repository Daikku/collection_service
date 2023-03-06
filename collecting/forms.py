from django import forms

from .models import City, Language


class CollectionForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  to_field_name='slug',
                                  required=False,
                                  widget=forms.Select(attrs={'class': "form-select mb-3"}),
                                  label='Город',
                                  empty_label='Выберите город')
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      to_field_name='slug',
                                      required=False,
                                      widget=forms.Select(attrs={'class': "form-select mb-3"}),
                                      label='Язык программирования',
                                      empty_label='Выберите язык программирования')
