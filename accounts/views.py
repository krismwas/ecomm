from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail


def guest_register_view(request):
    form = GuestForm(request.POST or None)

    context = {
        'form': form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    request_path = next_ or next_post or None

    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id

        if is_safe_url(request_path, request.get_host()):
            return redirect(request_path)
        else:
            return redirect('/')
    return redirect('/register/')


def login_page(request):
    form = LoginForm(request.POST)

    context = {
        'form': form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    request_path = next_ or next_post or None

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # print("mke nyumbani")
            # print(is_safe_url(request_path, request.get_host()))
            if is_safe_url(request_path, request.get_host()):
                return redirect(request_path)
            else:
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
