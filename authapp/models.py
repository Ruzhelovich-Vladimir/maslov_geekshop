from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class ShopUser(AbstractUser):

    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='аватар')
    age = models.PositiveIntegerField(verbose_name='возраст')

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def is_activation_key_expired(self):
        print(now(), self.activation_key_expires)
        return now() >= self.activation_key_expires


