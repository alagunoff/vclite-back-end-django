from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserManager(BaseUserManager):
    def create_user(self, username: str, first_name: str, password: None = None) -> "User":
        user: User = self.model(
            username=username,
            first_name=first_name
        )
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, username: str, first_name: str, password: None = None) -> "User":
        user = self.create_user(
            username,
            first_name,
            password,
        )
        user.is_admin = True
        user.save(using=self._db)

        return user


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class User(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self) -> bool:
        return self.is_admin
