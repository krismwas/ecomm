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
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sub_total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)

    objects = CartModelManager()

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver_signal(sender, instance, action, **kwargs):
    print("kl")
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        print('ml')
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.sub_total != total:
            instance.sub_total = total
            instance.save()


m2m_changed.connect(m2m_changed_cart_receiver_signal, sender=Cart.products.through)


def pre_save_cart_receiver_signal(sender, instance, **kwargs):
    # if instance.total > 0:
    #     print('pasquina')
    instance.total = instance.sub_total + 10
    # else:
    #     print('maouse')
    #     instance.total = 0.00


pre_save.connect(pre_save_cart_receiver_signal, sender=Cart)
