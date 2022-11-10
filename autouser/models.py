from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_user(self, email, password=None, **other_fields):
        if not email:
            raise ValueError("A email must be provided")

        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **other_fields):
        if password is None: 
            raise TypeError('Superusers must have a password')

        user = self.create_user(email, password)
        user.is_superuser = True 
        user.is_staff = True 
        user.save()
        return user


class AutoUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=20, blank=False)
    # photo = models.ImageField(upload_to='photos/autouser/', default="default_profile_pic")
    photo=models.ImageField(upload_to='photos/autouser/', default="default_profile_pic")
    start_date = models.DateField(auto_now=True)
    phone_number = models.CharField(max_length=50, blank=True, unique=False)
    email = models.CharField(max_length=50, blank=False, unique=True)
    password = models.CharField(max_length=128, null=False)
    is_technician = models.BooleanField(default=False)
    is_advertiser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class AutoUserFavourite(models.Model):
    auto_user = models.ManyToManyField(AutoUser, blank=True, related_name="autouserfavourite")
    technician = models.ManyToManyField(AutoUser, blank=True, related_name="technicianfavourite")
    date = models.DateField(auto_now=True)
