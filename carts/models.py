from django.db import models
from django.conf import settings

from products.models import Product


class CartModelManager(models.Manager):
    def new(self, user):
        return self.model.objects.create(user=user)


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartModelManager()

    def __str__(self):
        return str(self.id)

