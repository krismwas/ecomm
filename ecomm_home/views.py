from django.shortcuts import render, redirect

from .forms import ContactForm


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



