from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from srproj.accounts.managers import AccountManager
from srproj.common.validators import validate_name, validate_phone


class Company(models.Model):
    name = models.CharField(max_length=30,)
    contract_number = models.CharField(
        max_length=10,
        unique=True,
    )
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(
        default=True,
    )
    update_time = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.name}"
        # return f"{self.name} {self.contract_number} {self.is_active}"

    class Meta:
        ordering = ('update_time', 'is_active', 'name', 'contract_number')
        verbose_name_plural = "companies"


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True,)
    last_login = models.DateTimeField(auto_now_add=True,)
    is_staff = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)
    is_superuser = models.BooleanField(default=False,)
    is_external = models.BooleanField(default=True,)
    is_restricted = models.BooleanField(default=False,)
    company = models.ForeignKey(
        Company,
        on_delete=models.RESTRICT,
        # null=True,
        # blank=True,
    )

    objects = AccountManager()

    USERNAME_FIELD = "email"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class AccountProfile(models.Model):
    first_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        validators=(
            validate_name,
        )
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        validators=(
            validate_name,
        )
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        validators=(
            validate_phone,
        )
    )
    account = models.OneToOneField(
        Account,
        on_delete=models.RESTRICT,
        primary_key=True,
    )

    def get_full_name(self):
        first_name = "" if not self.first_name else self.first_name
        last_name = "" if not self.last_name else self.last_name
        full_name = f"{first_name} {last_name}"
        full_name = full_name.strip()
        return full_name if full_name else self.account.email

    def get_short_name(self):
        return self.first_name if self.first_name else None

    def __str__(self):
        full_name = self.get_full_name()
        full_name = "" if not full_name else full_name
        return full_name + self.account.email
