from django.conf.urls import url

from products.views import ProductList, ProductSlugDetail

urlpatterns = [
    url(r'^$', ProductList.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', ProductSlugDetail.as_view()),
    # url(r'^product-detail/(?P<pk>\d+)/$', ProductDetail.as_view()),


]
