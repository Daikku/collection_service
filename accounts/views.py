from django.shortcuts import render, redirect
from django.contrib.auth import  authenticate, login, logout

from .forms import UserLoginForm


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('home_page')
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home_page')