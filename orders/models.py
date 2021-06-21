from django.db import models
from django.db.models.signals import pre_save, post_save

from carts.models import Cart
from billing.models import BillingProfile
from ecomm_home.utils import unique_order_id_generator

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, null=True, blank=True)
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.99, max_digits=50, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = float(cart_total) + float(shipping_total)
        self.total = new_total
        self.save()
        return new_total


def post_save_order(instance, created, **kwargs):
    if created:
        instance.update_total()


post_save.connect(post_save_order, sender=Order)


def post_save_cart_total(instance, created, **kwargs):
    if not created:
        cart_obj = instance
        qs = Order.objects.filter(cart__id=cart_obj.id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def pre_save_unique_order_id(instance, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_unique_order_id, sender=Order)

