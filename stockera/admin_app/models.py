from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Create your models here.
# admin_app/models.py

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class IPOInfo(models.Model):
    company_logo_path = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255)
    price_band = models.CharField(max_length=255, blank=True, null=True)
    open = models.CharField(max_length=255, blank=True, null=True)
    close = models.CharField(max_length=255, blank=True, null=True)
    issue_size = models.CharField(max_length=255, blank=True, null=True)
    issue_type = models.CharField(max_length=255, blank=True, null=True)
    listing_date = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    ipo_price = models.CharField(max_length=255, blank=True, null=True)
    listing_price = models.CharField(max_length=255, blank=True, null=True)
    listing_gain = models.CharField(max_length=255, blank=True, null=True)
    cmp = models.CharField(max_length=255, blank=True, null=True)
    current_return = models.CharField(max_length=255, blank=True, null=True)
    rhp = models.CharField(max_length=255, blank=True, null=True)
    drhp = models.CharField(max_length=255, blank=True, null=True)

"""
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    staff_status = models.BooleanField(default=False)

    def __str__(self):
        return self.username
"""