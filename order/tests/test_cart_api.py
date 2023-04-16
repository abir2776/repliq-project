"""
Tests Cart API.
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core import models

from rest_framework.test import APIClient
from rest_framework import status
from order import serializers

orderItem_list_url = reverse("order:orderItem_list")
order_url = reverse("order:order_create")


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class CartAPITest(TestCase):
    """Testing Cart API"""

    def setUp(self):
        self.user = create_user(
            email="test@example.com",
            password="test1234",
        )
        self.cat = models.Category.objects.create(title="elections")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.shop = models.Shop.objects.create(
            name="Khan Store", user=self.user, category=self.cat, default=True
        )
        self.product = models.Product.objects.create(
            title="shirt", shop=self.shop, price=Decimal("50.5"), quantity=100
        )

    def test_add_to_cart(self):
        """Test if we can add a product to cart."""
        payload = {
            "product": self.product.id,
        }
        res = self.client.post(orderItem_list_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.OrderItems.objects.all().exists())

    def test_get_cart_list(self):
        """Test get all the the cart items."""
        models.OrderItems.objects.create(
            user=self.user, shop=self.shop, product=self.product
        )
        res = self.client.get(orderItem_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_place_order(self):
        """Test create place order."""
        test_product = models.Product.objects.create(
            title="pant", shop=self.shop, price=Decimal("50.5"), quantity=100
        )
        order1 = models.OrderItems.objects.create(
            user=self.user, shop=self.shop, product=self.product
        )
        order2 = models.OrderItems.objects.create(
            user=self.user, shop=self.shop, product=test_product
        )
        payload = {"orderitem": [order1.id, order2.id]}
        res = self.client.post(order_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.Order.objects.all().exists())
