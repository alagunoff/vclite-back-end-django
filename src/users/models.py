import binascii
import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from shared.utils import decode_base64_to_image

from .utils import get_user_avatar_directory_path


class Token(models.Model):
    token = models.CharField(max_length=40)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class UserManager(BaseUserManager):
    def create_user(self, username, password, **kwargs):
        extra_fields = {
            'first_name': kwargs.get('first_name')
        }

        avatar = kwargs.get('avatar')
        if avatar:
            extra_fields['avatar'] = decode_base64_to_image(avatar)

        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        Token.objects.create(token=binascii.hexlify(
            os.urandom(20)).decode(), user=user)

        return user

    def create_superuser(self, username, first_name, password, **kwargs):
        user = self.create_user(
            username,
            password,
            first_name=first_name,
            **kwargs
        )
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(
        max_length=30, blank=True, null=True)
    avatar = models.ImageField(upload_to=get_user_avatar_directory_path, blank=True,
                               default='users/user-picture-placeholder.jpg')
    creation_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name']
