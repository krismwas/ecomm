from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import Product
from carts.models import Cart


class ProductFeatured(ListView):
    queryset = Product.objects.featured()
    template_name = 'products/featured.html'


class ProductList(ListView):
    queryset = Product.objects.all()
    # model = Product
    template_name = 'products/list.html'


class ProductDetail(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_object(self, *args, **kwargs):
        # request = self.request
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404('product does not exist')
        return instance


class ProductSlugDetail(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_object(self, *args, **kwargs):
        # request = self.request
        slug = self.kwargs.get('slug')
        instance = Product.objects.get_by_slug(slug)
        if instance is None:
            raise Http404('product does not exist')
        return instance

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context


def product_detail_view(request, pk):
    qs = Product.objects.filter(id=pk)
    instance = Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404('product does not exist')
    print("0000000000000")
    print(instance)
    context = {
        'object': instance
    }
    return render(request, 'products/detail.html', context)


