from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegisterForm


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
    return render(request, 'auth/login.html', context)


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
    return render(request, 'auth/register.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    context = {
        'form': contact_form,
        'title': 'contact page',
        'content': 'Welcome to the content page'
    }
    return render(request, 'contact/view.html', context)


def home_page(request):
    context = {
        'title': 'Home page',
        'content': 'Welcome to the home page'
    }
    return render(request, 'home_page.html', context)



