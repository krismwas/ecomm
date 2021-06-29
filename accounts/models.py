from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.template.loader import get_template
from django.core.mail import send_mail

from ecomm_home.utils import unique_key_generator


class MyUserManager(BaseUserManager):

    def create_user(self, email, full_name=None, password=None, is_active=False, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        # if not full_name:
        #     raise ValueError("User must have a full name")
        user_obj = self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)

    def create_staff_user(self, email, full_name=None, password=None):
        user_obj = self.create_user(
            email, full_name, password=password, is_staff=True
        )
        return user_obj

    def create_superuser(self, email, full_name=None, password=None):
        user_obj = self.create_user(
            email, full_name, password=password, is_staff=True, is_admin=True, is_active=True
        )
        return user_obj


class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    # active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.active


# class Profile(models.Model):
#     user = models.OneToOneField(MyUser)

class EmailActivation(models.Model):
    user = models.ForeignKey(MyUser)
    email = models.EmailField()
    key = models.CharField(max_length=120, blank=True, null=True)
    activated = models.BooleanField(default=False)
    force_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_email_activation(self):
        if not self.activated and not self.force_expired:
            if self.key:
                base_url = settings.BASE_URL
                # base_url = getattr(settings, 'BASE_URL', 'http/kdkdkdkdk.co.ke')
                key_path = self.key
                path_ = f"{base_url}/{key_path}"
                context = {
                    'path': path_,
                    'email': self.email
                }
                txt_ = get_template('registration/emails/verify.txt').render(context)
                html_ = get_template('registration/emails/verify.html').render(context)
                subject = '1 click Email verification'
                from_email = 'This sender'
                recipient_list = [self.email]
                sent_email = send_mail(
                    subject, txt_, from_email, recipient_list, html_message=html_, fail_silently=False
                )
                return sent_email
        return False


def pre_save_email_activation(instance, **kwargs):
    if not instance.activated and not instance.force_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)


pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_create_receiver(instance, created, **kwargs):
    if created:
        myuser_obj = instance
        obj = EmailActivation.objects.create(user=myuser_obj, email=myuser_obj.email)
        obj.send_email_activation()


post_save.connect(post_save_user_create_receiver, sender=MyUser)


class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
