"""
Tests Product API.
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core import models
import tempfile
import os
from PIL import Image

from rest_framework.test import APIClient
from rest_framework import status

product_list_url = reverse("store:product_list")
find_product_url = reverse("store:find_product")


def product_detail_url(slug):
    return reverse("store:product_detail", args=[slug])


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class ProductAPITest(TestCase):
    """Test all private api of product model.."""

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

    def test_create_product(self):
        """Testing if a user can create a product or not."""
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {
                "title": "Jeans pant",
                "shop": self.shop.id,
                "price": Decimal("500.50"),
                "quantity": 100,
                "image": image_file,
            }
            res = self.client.post(product_list_url, payload)
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            self.assertTrue(models.Product.objects.all().exists())

    def test_get_all_products(self):
        """Testing getting all products created by logged in shop."""
        models.Product.objects.create(
            title="shirt", shop=self.shop, price=Decimal("50.5"), quantity=100
        )
        models.Product.objects.create(
            title="pants", shop=self.shop, price=Decimal("50.5"), quantity=100
        )
        models.Product.objects.create(
            title="shorts", shop=self.shop, price=Decimal("50.5"), quantity=100
        )
        models.Product.objects.create(
            title="pajama", shop=self.shop, price=Decimal("50.5"), quantity=100
        )

        res = self.client.get(product_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)

    def test_get_product_detail(self):
        """Test get single product detail."""
        product = models.Product.objects.create(
            title="shirt", shop=self.shop, price=Decimal("50.5"), quantity=100
        )
        res = self.client.get(product_detail_url(product.slug))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], product.title)

    def test_update_product_details(self):
        """Test Update single product details.."""
        product = models.Product.objects.create(
            title="shirt", shop=self.shop, price=Decimal("50.5"), quantity=100
        )
        payload = {
            "title": "pant",
            "quantity": 80,
        }
        res = self.client.patch(product_detail_url(product.slug), payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["title"], payload["title"])
        self.assertEqual(res.data["quantity"], payload["quantity"])

    def test_delete_a_product(self):
        """Test delete a product."""
        product = models.Product.objects.create(
            title="shirt", shop=self.shop, price=Decimal("50.5"), quantity=100
        )
        res = self.client.delete(product_detail_url(product.slug))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Product.objects.all().exists())

    def test_get_product_by_friendship(self):
        """Test get all products by friendship."""
        test_shop = models.Shop.objects.create(
            name="goni store", user=self.user, category=self.cat
        )
        test_shop2 = models.Shop.objects.create(
            name="goni store2", user=self.user, category=self.cat
        )
        models.UserGroup.objects.create(
            sender=test_shop, receiver=self.shop, status="accepted"
        )
        models.Product.objects.create(
            title="shirt", shop=test_shop, price=Decimal("50.5"), quantity=100
        )
        models.Product.objects.create(
            title="pants", shop=test_shop, price=Decimal("50.5"), quantity=100
        )
        models.Product.objects.create(
            title="shorts", shop=test_shop, price=Decimal("50.5"), quantity=100
        )
        models.Product.objects.create(
            title="pajama", shop=test_shop, price=Decimal("50.5"), quantity=100
        )
        models.Product.objects.create(
            title="katua", shop=test_shop2, price=Decimal("50.5"), quantity=100
        )

        res = self.client.get(find_product_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)
