from django.shortcuts import render
from .models import Cart
# Create your views here.


def cart_home(request):
    request.session['cart_id'] = '12'
    cart_id = request.session.get('cart_id', None)
    # if cart_id is None:
    #     cart_obj = Cart.objects.create(user=None)
    #     request.session['cart_id'] = cart_obj.id

    qs = Cart.objects.filter(id=cart_id)
    if qs.count() == 1:
        print('cart_id exists')
        cart_obj = qs.first()
    else:
        cart_obj = Cart.objects.create(user=None)
        request.session['cart_id'] = cart_obj.id

    context = {}
    return render(request, 'carts/home.html', context)
