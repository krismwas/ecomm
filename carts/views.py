from django.shortcuts import render, redirect

from products.models import Product
from .models import Cart

# Create your views here.


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {}
    return render(request, 'carts/home.html', context)


def cart_update(request):
    product_obj = Product.objects.get(id=1)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    cart_obj.products.add(product_obj)
    return redirect("cart:home")

