from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid
from autoslug import AutoSlugField


class BaseModelWithUID(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModelWithUID):
    """Category object"""

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModelWithUID):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to="profile_pic", blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"


class Shop(BaseModelWithUID):
    """Shop model"""
    default = models.BooleanField(default=False)
    name = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255,blank=True)
    ph_no = models.CharField(max_length=20,blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name="categorys",
        blank=True,
        null=True,
    )


class UserGroup(BaseModelWithUID):
    """Create a new user group"""

    CHOICES = (
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("pending", "Pending"),
    )
    sender = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="senders"
    )
    receiver = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="receivers"
    )
    status = models.CharField(max_length=15, choices=CHOICES)

    def __str__(self):
        return self.status


class Product(BaseModelWithUID):
    """Create a new Product"""

    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5,decimal_places=2)
