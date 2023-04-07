"""
Tests category api.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core import models

from rest_framework.test import APIClient
from rest_framework import status

CAT_URL = reverse('store:category-create')

def detail_url(category_id):
    return reverse('store:category-detail', args=[category_id])

def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_superuser(**params)

class PublicApiTest(TestCase):
    """Test the public API of the store api."""
    def test_pemission_on_category_create(self):
        payload = {
            'title':'electronics',
        }
        res = self.client.post(CAT_URL, payload)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateApiTest(TestCase):
    """Test the private API or the srore api."""
    def setUp(self):
        self.user = create_user(
            email = 'test@example.com',
            password = 'test1234',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_superuser_can_create_category(self):
        payload = {
            'title':'electronic',
        }
        res = self.client.post(CAT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    def test_category_update(self):
        cat = models.Category.objects.create(title='electronic')
        url = detail_url(cat.id)
        payload = {
            'title':'electronics',
        }
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        cat.refresh_from_db()
        self.assertEqual(cat.title, payload['title'])

    def test_category_delete(self):
        cat = models.Category.objects.create(title='electronics')
        url = detail_url(cat.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Category.objects.filter(id=cat.id).exists())
