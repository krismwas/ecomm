from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from addresses.forms import AddressForm


def checkout_address_create_view(request):
    form = AddressForm(request.POST or None)
    context = {
        'form': form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    request_path = next_ or next_post or None
    if form.is_valid():

        if is_safe_url(request_path, request.get_host()):
            return redirect(request_path)
        else:
            return redirect('cart:check_out')
    return redirect('cart:check_out')
