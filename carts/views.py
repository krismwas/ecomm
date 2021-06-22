from django.shortcuts import render, redirect

from products.models import Product
from addresses.forms import AddressForm
from orders.models import Order
from addresses.models import Adress
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
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


def checkout_home(request):
    cart_obj, cart_obj_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_obj_created or cart_obj.products.count() == 0:
        return redirect('cart:home')
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Adress.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address = Adress.objects.get(id=billing_address_id)
            del request.session['billing_address_id ']
        if billing_address_id or shipping_address_id:
            order_obj.save()

    context = {
        "login_form": login_form,
        "object": order_obj,
        "billing_profile": billing_profile,
        "guest_form": guest_form,
        "address_form": address_form,
        # "billing_address_form": billing_address_form
    }

    return render(request, 'carts/checkout.html', context)
