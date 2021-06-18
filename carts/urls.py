from django.conf.urls import url

from .views import cart_home, cart_update, checkout

urlpatterns = [
    url(r'^$', cart_home, name='home'),
    url(r'^update/$', cart_update, name='update'),
    url(r'^checkout/$', checkout, name='check_out'),
    # url(r'^product-detail/(?P<pk>\d+)/$', ProductDetail.as_view()),

]
