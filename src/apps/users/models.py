from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from rest_framework.authtoken.models import Token

from .constants import DEFAULT_USER_BASE64_AVATAR


class UserManager(BaseUserManager):
    def create_user(self, **kwargs) -> 'User':
        user: User = self.model(**kwargs)
        user.set_password(kwargs.get('password'))
        user.save(using=self.db)
        Token.objects.create(user=user)

        return user

    def create_superuser(self, username, first_name, password) -> 'User':
        user = self.create_user(
            username=username,
            password=password,
            first_name=first_name,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(
        max_length=30, blank=True, null=True)
    avatar = models.CharField(
        max_length=900000, default=DEFAULT_USER_BASE64_AVATAR)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        db_table = 'users'

    @property
    def is_staff(self) -> bool:
        return self.is_admin
