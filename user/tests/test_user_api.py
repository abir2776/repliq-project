"""
Tests user api
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from core import models

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token_obtain_pair')
ME_URL = reverse('user:me')
user_list_url = reverse('user:user_list')
grouping_request_url = reverse('user:grouping_requests')


def user_grp_url(user_uid):
    return reverse('user:user_grp',args=[user_uid])


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password is less than 5 chars."""
        payload = {
            'email':'test@example.com',
            'password':'pw',
            'name':'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test1234'
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrive_user_unauthorized(self):
        """Test authorization is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = create_user(
            email = 'test@example.com',
            password = 'test1234',
            name = 'Test User'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })
    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_of_users_by_category(self):
        """Test Showing user list by their category"""
        cat = models.Category.objects.create(title='electronic')
        cat2 = models.Category.objects.create(title='fashion')
        user1 = create_user(email='user1@example.com', password='newpassword123', category=cat, name='osman')
        user2 = create_user(email='user2@example.com', password='12345', category=cat, name='goni')
        user3 = create_user(email='user3@example.com', password='12345', category=cat2, name='abir')
        self.user.category = cat
        res = self.client.get(user_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),2)

    def test_create_user_group(self):
        """Test creating a user group."""
        test_user = create_user(email='user@example.com', password='12345' , name='exampleuser')

        res = self.client.post(user_grp_url(test_user.uid))

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(models.UserGroup.objects.filter(sender=self.user).exists())

    def test_show_grouping_requests(self):
        """Test showing all grouping requests."""
        user1 = create_user(email='user1@example.com', password='12345')
        user2 = create_user(email='user2@example.com', password='12345')
        user3 = create_user(email='user3@example.com', password='12345')

        models.UserGroup.objects.create(sender=user1,receiver=self.user,status='pending')
        models.UserGroup.objects.create(sender=user2,receiver=self.user,status='pending')
        models.UserGroup.objects.create(sender=user3,receiver=self.user,status='pending')

        res = self.client.get(grouping_request_url)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),3)
