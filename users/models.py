from uuid import uuid4
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now


class UserManager(BaseUserManager):
    """
    This manager helps in the creation of users and listing of users
    """

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email), first_name=first_name, last_name=last_name, **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name=None, last_name=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        self.model.REQUIRED_FIELDS.append("first_name")
        self.model.REQUIRED_FIELDS.append("last_name")
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            **extra_fields
        )
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    This model handles operation on the user table
    """
    NATIONAL_ID = 'NID'
    PASSPORT = 'PSP'
    IDENTIFICATION_TYPE = (
        (NATIONAL_ID, "Nation ID"),
        (PASSPORT, "Passport"),
    )
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    identification_type = models.CharField(
        max_length=3, choices=IDENTIFICATION_TYPE, default=NATIONAL_ID)
    identification = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(null=True)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)

    joined_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'identification_type',
        'identification',
    ]

    def __str__(self) -> str:
        return f"{self.first_name} ${self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self):
        return bool(self.active and not self.is_suspended)

    @property
    def is_staff(self):
        return self.staff

    @property
    def has_account(self):
        if hasattr(self, 'account'):
            return True
        return False


class UserAdditionalInfo(models.Model):
    """
    any additional information about the user willl be stored via this model
    """
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(
        User, related_name="information", on_delete=models.CASCADE)
    country = models.CharField(max_length=50, null=True, blank=True)
    province = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    phone_number1 = models.CharField(max_length=30, unique=True)
    phone_number2 = models.CharField(max_length=30, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()


class OTP(models.Model):
    """
    This OTP model is used for verifying the user email
    """
    REGISTRATION = 'REG'
    RESET_PASSWORD = 'REP'

    OTP_TYPE_CHOICES = (
        (REGISTRATION, "Registration"),
        (RESET_PASSWORD, "Reset password"),
    )
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    code = models.CharField(unique=True, max_length=6)
    user = models.ForeignKey(
        User, related_name='verification_codes', on_delete=models.CASCADE, null=True)
    otp_type = models.CharField(max_length=5)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @property
    def is_valid(self):
        return bool(self.is_active and now() < self.created_on+settings.OTP_LIFETIME)
