import hashlib

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    """
    Менеджер пользователей для кастомной модели пользователя.

    Методы:
    create_user(self, email, password, **extra_fields): Создает и сохраняет пользователя с указанными данными.
    create_superuser(self, email, password, **extra_fields): Создает и сохраняет суперпользователя с указанными данными.
    """

    use_in_migration = True

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
        Кастомная модель пользователя
    """
    username = None
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    activation_code = models.CharField(max_length=50, blank=True)

    objects = MyUserManager()

    class Meta:
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def create_activation_code(self):
        """
        Создает код активации пользователя на основе его электронного адреса и идентификатора.
        """

        string = self.email + str(self.id)
        encode_string = string.encode()
        md5_object = hashlib.md5(encode_string)
        activation_code = md5_object.hexdigest()
        self.activation_code = activation_code

    def __str__(self):
        return self.email
