from django.shortcuts import render
from django.views.generic.list import ListView

from products.models import Product

# Create your views here.


class ProductSearchView(ListView):
    queryset = Product.objects.all()
    # model = Product
    template_name = 'search/view.html'

    # def get_context_data(self, **kwargs):
    #     # query = self.request.GET.get('q')
    #     context = super().get_context_data(**kwargs)
    #     context['query'] = self.request.GET.get('q')
    #     print("gggggggggggggggggggggg")
    #     print(self.request.GET.get('q'))
    #     return context

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        if query:
            p = self.queryset.filter(title__icontains=query)
            if p.exists():
                return p
        return Product.objects.featured()

        # print(self.request.GET)
        # print('nnnnnn')
        # print(query)
        # print('nnnnnnn')
        # if query is not None:
        #     p = self.queryset.filter(title__icontains=query)
        #     print(p)
        #     print(p.exists())
        #     if p.exists():
        #         print("anita")
        #         return p
        # print("kamau")
        # return Product.objects.featured()





