from django.shortcuts import render, redirect

from products.models import Product
from .models import Cart

# Create your views here.


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    context = {"cart": cart_obj}
    return render(request, 'carts/home.html', context)


def cart_update(request):
    product_id = request.POST.get('product_id', None)
    if product_id is not None:
        product_obj = Product.objects.get(id=product_id)
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_item'] = cart_obj.products.count()
    return redirect("cart:home")

