from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import uuid
from autoslug import AutoSlugField
from versatileimagefield.fields import VersatileImageField
from django.dispatch import receiver
from django.db.models.signals import pre_save


class BaseModelWithUID(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
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
    address = models.CharField(max_length=255, blank=True)
    ph_no = models.CharField(max_length=20, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name="categorys",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class UserGroup(BaseModelWithUID):
    """Create a new user group"""

    CHOICES = (
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("pending", "Pending"),
    )
    sender = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="senders")
    receiver = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="receivers"
    )

    class Meta:
        unique_together = ("sender", "receiver")

    status = models.CharField(max_length=15, choices=CHOICES)

    def __str__(self):
        return f"Sender: {self.sender}, Receiver: {self.receiver}"


class Product(BaseModelWithUID):
    """Create a new Product"""

    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="title")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = VersatileImageField(upload_to="product_image/", blank=True)

    def __str__(self):
        return self.title


class OrderItems(BaseModelWithUID):
    """When user add product to cart all products will here in this model.."""

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return f"{self.quantity} X {self.product}"


class Order(BaseModelWithUID):
    orderitem = models.ManyToManyField(OrderItems)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    order_id = models.PositiveIntegerField(unique=True)

    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += float(order_item.get_total())
        return total


def generate_order_id():
    last_order = Order.objects.all().order_by("order_id").last()
    if not last_order:
        return 1
    return last_order.order_id + 1


@receiver(pre_save, sender=Order)
def set_order_id(sender, instance, **kwargs):
    if not instance.order_id:
        instance.order_id = generate_order_id()
