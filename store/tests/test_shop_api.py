"""
Tests shop api.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core import models

from rest_framework.test import APIClient
from rest_framework import status

shop_list_url = reverse('store:shop_list')
find_shop_url = reverse('store:find_shop')

def shop_detail_url(uid):
    return reverse('store:shop_detail', args=[uid])

def shop_login_url(uid):
    return reverse('store:shop_login', args=[uid])

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
        self.cat = models.Category.objects.create(title='elections')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_shop(self):
        """Test creating a shop."""
        cat = models.Category.objects.create(title='test_category')
        payload = {
            'name':'Khan store',
            'category':cat.id,
        }
        res = self.client.post(shop_list_url, payload)
        # print('Response:',res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], payload['name'])

    def test_getting_shop_list(self):
        """Test showing a shop list."""
        res = self.client.get(shop_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_getting_shop_detail(self):
        """Test showing a individual shop."""
        cat = models.Category.objects.create(title='electronics')
        shop = models.Shop.objects.create(name='Khan store', user=self.user, category=cat)

        res = self.client.get(shop_detail_url(shop.uid))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], 'Khan store')

    def test_shop_full_update(self):
        """Test updating all shop fields."""
        shop = models.Shop.objects.create(name='khan store', user=self.user, category=self.cat)
        test_cat = models.Category.objects.create(title='Books')
        test_user = create_user(email='testuser@example.com', password='testpassword')
        payload = { 'name':'testshop', 'category':test_cat.id, 'user':test_user.id }

        res = self.client.put(shop_detail_url(shop.uid), payload)

        shop.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], payload['name'])
    def test_shop_partial_update(self):
        """Testing shop partial update."""
        shop = models.Shop.objects.create(name='khan store', user=self.user, category=self.cat)
        payload = { 'name':'testshop' }

        res = self.client.patch(shop_detail_url(shop.uid), payload)
        # print('REsponse: ' , res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], payload['name'])

    def test_delete_shop(self):
        """Test deleting a shop."""
        shop = models.Shop.objects.create(name='khan store', user=self.user, category=self.cat)

        res = self.client.delete(shop_detail_url(shop.uid))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Shop.objects.all().exists())

    def test_show_shop_by_category(self):
        """Test show shop by category.."""
        test_cat = models.Category.objects.create(title = 'test_category')
        models.Shop.objects.create(name='khan store', user=self.user, category=self.cat, default=True)
        models.Shop.objects.create(name='khan store', user=self.user, category=self.cat)
        models.Shop.objects.create(name='khan store', user=self.user, category=self.cat)
        models.Shop.objects.create(name='khan store', user=self.user, category=test_cat)
        models.Shop.objects.create(name='khan store2', user=self.user, category=self.cat)

        res = self.client.get(find_shop_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)

    def test_login_to_shop(self):
        """Test login to a shop."""
        shop1 = models.Shop.objects.create(name='test shop', user=self.user, category=self.cat)
        shop2 = models.Shop.objects.create(name='test shop2', user=self.user, category=self.cat)
        res = self.client.patch(shop_login_url(shop1.uid))
        shop2.refresh_from_db()
        shop1.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(shop2.default, False)
        self.assertEqual(shop1.default, True)

