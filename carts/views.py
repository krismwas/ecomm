from django.shortcuts import render

from products.models import Product
from .models import Cart

# Create your views here.


def cart_home(request):

    cart_obj, new_obj = Cart.objects.new_or_get(request)

    context = {}
    return render(request, 'carts/home.html', context)
