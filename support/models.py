from enum import Enum

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CountriesChoices(Enum):
    RS = 'Serbia'
    HR = 'Croatia'


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, country, password = None, is_admin=False, is_staff=False):
        if not email:
            raise ValueError("User must have an email!")

        if not password:
            raise ValueError("User must have a password!")

        user_object = self.model(
            email=self.normalize_email(email)
        )

        user_object.set_password(password)
        user_object.admin = is_admin
        user_object.staff = is_staff
        user_object.save(using=self.db)

        return user_object

    def create_staffuser(self, email, first_name, last_name, country, password):
        return self.create_user(email, first_name, last_name, country, password, True, True)

    def create_superuser(self, email, first_name, last_name, country, password):
        return self.create_user(email, first_name, last_name, country, password, True, True)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, null=False)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    country = models.CharField(max_length=128, choices=[(tag.value, tag.value) for tag in CountriesChoices])
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)

    # Koristimo email kao username
    USERNAME_FIELD = 'email'

    # Zahtevamo nova polja koja smo dodali da budu pristuna (email i password se podrazumevaju)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'country']

    object = UserManager()

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def __str__(self):
        return self.email


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    product = models.CharField(max_length=128)
    content = models.CharField(max_length=2048)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TicketAnswers(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)

