from django.shortcuts import render

# Create your views here.


def cart_home(request):
    context = {}
    return render(request, 'carts/home.html', context)
