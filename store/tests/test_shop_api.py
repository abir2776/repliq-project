"""
Tests shop api.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core import models

from rest_framework.test import APIClient
from rest_framework import status

shop_list_url = reverse("store:shop_list")
find_shop_url = reverse("store:find_shop")
request_url = reverse("store:request_list")
my_friends_url = reverse("store:my_friends")
my_requests_url = reverse("store:my_requests")


def shop_detail_url(uid):
    return reverse("store:shop_detail", args=[uid])


def shop_login_url(uid):
    return reverse("store:shop_login", args=[uid])


def request_detail_url(uid):
    return reverse("store:request_detail", args=[uid])


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class ShopApiTest(TestCase):
    """Create public shop api test"""

    def setUp(self):
        self.user = create_user(
            email="test@example.com",
            password="test1234",
        )
        self.cat = models.Category.objects.create(title="elections")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_shop(self):
        """Test creating a shop."""
        cat = models.Category.objects.create(title="test_category")
        payload = {
            "name": "Khan store",
            "category": cat.id,
        }
        res = self.client.post(shop_list_url, payload)
        # print('Response:',res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["name"], payload["name"])

    def test_getting_shop_list(self):
        """Test showing a shop list."""
        res = self.client.get(shop_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_getting_shop_detail(self):
        """Test showing a individual shop."""
        cat = models.Category.objects.create(title="electronics")
        shop = models.Shop.objects.create(
            name="Khan store", user=self.user, category=cat
        )

        res = self.client.get(shop_detail_url(shop.uid))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], "Khan store")

    def test_shop_full_update(self):
        """Test updating all shop fields."""
        shop = models.Shop.objects.create(
            name="khan store", user=self.user, category=self.cat
        )
        test_cat = models.Category.objects.create(title="Books")
        test_user = create_user(email="testuser@example.com", password="testpassword")
        payload = {"name": "testshop", "category": test_cat.id, "user": test_user.id}

        res = self.client.put(shop_detail_url(shop.uid), payload)

        shop.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], payload["name"])

    def test_shop_partial_update(self):
        """Testing shop partial update."""
        shop = models.Shop.objects.create(
            name="khan store", user=self.user, category=self.cat
        )
        payload = {"name": "testshop"}

        res = self.client.patch(shop_detail_url(shop.uid), payload)
        # print('REsponse: ' , res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], payload["name"])

    def test_delete_shop(self):
        """Test deleting a shop."""
        shop = models.Shop.objects.create(
            name="khan store", user=self.user, category=self.cat
        )

        res = self.client.delete(shop_detail_url(shop.uid))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_show_shop_by_category(self):
        """Test show shop by category.."""
        test_cat = models.Category.objects.create(title="test_category")
        models.Shop.objects.create(
            name="khan store", user=self.user, category=self.cat, default=True
        )
        models.Shop.objects.create(name="khan store", user=self.user, category=self.cat)
        models.Shop.objects.create(name="khan store", user=self.user, category=self.cat)
        models.Shop.objects.create(name="khan store", user=self.user, category=test_cat)
        models.Shop.objects.create(
            name="khan store2", user=self.user, category=self.cat
        )

        res = self.client.get(find_shop_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)

    def test_login_to_shop(self):
        """Test login to a shop."""
        shop1 = models.Shop.objects.create(
            name="test shop", user=self.user, category=self.cat
        )
        shop2 = models.Shop.objects.create(
            name="test shop2", user=self.user, category=self.cat
        )
        res = self.client.patch(shop_login_url(shop1.uid))
        shop2.refresh_from_db()
        shop1.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(shop2.default, False)
        self.assertEqual(shop1.default, True)

    def test_sending_grouping_request(self):
        """Test sending grouping request to buy and sell products."""
        test_user = create_user(email="testuser@example.com", password="testpassword")
        test_shop = models.Shop.objects.create(
            name="test_shop", user=test_user, category=self.cat, default=False
        )
        shop = models.Shop.objects.create(
            name="Khan store", user=self.user, category=self.cat, default=True
        )
        payload = {
            "sender": shop.id,
            "receiver": test_shop.id,
            "status": "pending",
        }
        res = self.client.post(request_url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.UserGroup.objects.all().exists())

    def test_showing_list_of_requests(self):
        """Test showing all requests send to a shop from another shops."""
        test_user = create_user(email="testuser@example.com", password="testpassword")
        test_shop1 = models.Shop.objects.create(
            name="test_shop1", user=test_user, category=self.cat
        )
        test_shop2 = models.Shop.objects.create(
            name="test_shop2", user=test_user, category=self.cat
        )
        shop = models.Shop.objects.create(
            name="Khan store", user=self.user, category=self.cat, default=True
        )
        models.UserGroup.objects.create(
            sender=test_shop1, receiver=shop, status="pending"
        )
        models.UserGroup.objects.create(
            sender=test_shop2, receiver=shop, status="pending"
        )

        res = self.client.get(request_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_showing_request_details(self):
        """Test the details of a request."""
        test_user = create_user(email="testuser@example.com", password="testpassword")
        shop1 = models.Shop.objects.create(user=self.user, category=self.cat)
        shop2 = models.Shop.objects.create(user=test_user, category=self.cat)
        request = models.UserGroup.objects.create(
            sender=shop1, receiver=shop2, status="pending"
        )
        res = self.client.get(request_detail_url(request.uid))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_editing_request_detail(self):
        """Test editing request details."""
        test_user = create_user(email="testuser@example.com", password="testpassword")
        shop1 = models.Shop.objects.create(user=self.user, category=self.cat)
        shop2 = models.Shop.objects.create(user=test_user, category=self.cat)
        request = models.UserGroup.objects.create(
            sender=shop1, receiver=shop2, status="pending"
        )

        payload = {"status": "accepted"}
        res = self.client.patch(request_detail_url(request.uid), payload)
        request.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(request.status, payload["status"])

    def test_delete_request(self):
        """Test deleting a request."""
        test_user = create_user(email="testuser@example.com", password="testpassword")
        shop1 = models.Shop.objects.create(user=self.user, category=self.cat)
        shop2 = models.Shop.objects.create(user=test_user, category=self.cat)
        request = models.UserGroup.objects.create(
            sender=shop1, receiver=shop2, status="pending"
        )

        res = self.client.delete(request_detail_url(request.uid))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.UserGroup.objects.all().exists())
        
    def test_show_all_friend_shop(self):
        """Test Showing all connected shops"""
        test_user = create_user(email="testuser@example.com", password="testpassword")
        shop1 = models.Shop.objects.create(user=test_user, category=self.cat, name="testshop1")
        shop2 = models.Shop.objects.create(user=test_user, category=self.cat, name="testshop2")
        shop3 = models.Shop.objects.create(user=test_user, category=self.cat, name="testshop3")
        shop4 = models.Shop.objects.create(user=self.user, category=self.cat, name="testshop4",default=True)
        models.UserGroup.objects.create(sender=shop4, receiver=shop2, status="accepted")
        models.UserGroup.objects.create(sender=shop4, receiver=shop3, status="accepted")
        models.UserGroup.objects.create(sender=shop4, receiver=shop1, status="accepted")
        
        res = self.client.get(my_friends_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),3)
        
    def test_show_my_requests(self):
        """Test showing all request send by logged in user."""
        test_user = create_user(email="testuser@example.com", password="testpassword")
        shop1 = models.Shop.objects.create(user=test_user, category=self.cat, name="testshop1")
        shop2 = models.Shop.objects.create(user=test_user, category=self.cat, name="testshop2")
        shop3 = models.Shop.objects.create(user=test_user, category=self.cat, name="testshop3")
        shop4 = models.Shop.objects.create(user=self.user, category=self.cat, name="testshop4",default=True)
        models.UserGroup.objects.create(sender=shop4, receiver=shop2, status="pending")
        models.UserGroup.objects.create(sender=shop4, receiver=shop3, status="pending")
        models.UserGroup.objects.create(sender=shop4, receiver=shop1, status="pending")
        
        res = self.client.get(my_requests_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),3)