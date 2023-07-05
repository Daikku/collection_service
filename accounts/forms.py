from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username').strip()
        password = self.cleaned_data.get('password').strip()

        if username and password:
            queryset = User.objects.filter(username=username)
            if not queryset.exists():
                raise forms.ValidationError('Username is not exist!')
            if not check_password(password, queryset[0].password):
                raise forms.ValidationError('Password is not correct!')
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('User is not active.')
        return super(UserLoginForm, self).clean(*args, **kwargs)