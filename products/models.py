import random
import os

from django.db import models
from django.db.models.signals import pre_save
from django.db.models import Q

from products.utils import unique_slug_generator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return ext


def upload_image_path(instance, filename):
    new_file_name = random.randint(1, 2398731)
    ext = get_filename_ext(filename)
    return f'products/{new_file_name}{ext}'


class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def get_by_id(self, id):
        qs = self.get_queryset().filter(pk=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()
        return None

    def featured(self):
        return self.get_queryset().filter(featured=True)

    def all(self):
        return self.get_queryset().active()

    def search(self, query):
        looks_ups = Q(title__icontains=query) | Q(description__icontains=query) | Q(tag__title__icontains=query)
        return Product.objects.filter(looks_ups).distinct()


class Product(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=False)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/products/{self.slug}/'


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
