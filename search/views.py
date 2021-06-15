from django.shortcuts import render
from django.views.generic.list import ListView

from products.models import Product

# Create your views here.


class ProductSearchView(ListView):
    queryset = Product.objects.all()
    # model = Product
    template_name = 'search/view.html'

    def get_queryset(self, *args, **kwargs):
        print(self.request.GET)
        query = self.request.GET.get('q')
        print("kkkkkkkkkkkkkkkkk")
        print(query)
        if query is not None:
            return self.queryset.filter(title__icontains=query)
            # return Product.objects.filter(title__icontains=query)
        return Product.objects.featured()





