import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.http import HttpResponseForbidden


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name,  password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name,  password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, last_name,  password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('student', 'STUDENT'),
        ('teacher', 'TEACHER'),
        ('school_admin', 'SCHOOL_ADMIN'),
        ('deputy_head', 'DEPUTY_HEAD'),
        ('school_head', 'SCHOOL_HEAD'),
        ('district_admin', 'DISTRICT_ADMIN'),
    )

    POSITION = (
        ('admin', 'ADMIN'),
        ('user', 'USER'),
        ('staff', 'STAFF'),
        ('student', 'STUDENT'),
    )

    email       = models.EmailField(unique=True)
    first_name  = models.CharField(max_length=30)
    last_name   = models.CharField(max_length=30)
    position    = models.CharField(max_length=30, choices=POSITION)
    user_type   = models.CharField(max_length=30, choices=USER_TYPE)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_school_superuser = models.BooleanField(default=False)
    objects     = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.set_password('munyaradzi')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


