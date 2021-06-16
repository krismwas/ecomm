from django.db import models
from django.conf import settings
from django.db.models.signals import m2m_changed, pre_save
from products.models import Product


class CartModelManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            print('cart_id exists')
            cart_obj = qs.first()
            new_obj = False
            if request.user.is_authenticated() and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated():
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartModelManager()

    def __str__(self):
        return str(self.id)


def pre_save_cart_receiver_signal(sender, instance, **kwargs):
    if instance.total > 0:
        instance.total = instance.sub_total + 10
    instance.total = 0.00


pre_save.connect(pre_save_cart_receiver_signal, sender=Cart)


def m2m_changed_cart_receiver_signal(sender, instance, action, **kwargs):
    cart_products = instance.products.all()
    sub_total = 0
    for product in cart_products:
        sub_total = + product.price
    if instance.sub_total == instance.total:
        instance.sub_total = sub_total
        instance.save()


m2m_changed.connect(m2m_changed_cart_receiver_signal, sender=Cart.products.through)
