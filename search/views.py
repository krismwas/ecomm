from django.db.models import Q
from django.views.generic.list import ListView

from products.models import Product

# Create your views here.


class ProductSearchView(ListView):
    queryset = Product.objects.all()
    template_name = 'search/view.html'

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get('q')
        if query:
            looks_ups = Q(title__icontains=query) | Q(description__icontains=query)
            p = self.queryset.filter(looks_ups)
            if p.exists():
                return p
        return Product.objects.featured()







