from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect

from .forms import LoginForm, RegisterForm


def login_page(request):
    form = LoginForm(request.POST)

    context = {
        'form': form
    }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            print('Error')
    return render(request, 'accounts/login.html', context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')

        new_user = get_user_model().objects.create_user(
            email, password, username
        )
        print(new_user)
    return render(request, 'accounts/register.html', context)
