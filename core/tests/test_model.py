"""
Tests for model
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def create_user(email='user@example.com', password='12345'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email,password)

class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@Example.com','Test2@example.com'],
            ['TEST3@EXAMPLE.COM','TEST3@example.com'],
            ['test4@example.COM','test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email,'sample123')
            self.assertEqual(user.email,expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError.."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')


    def test_create_superuser(self):
        """Test creating superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    def test_create_category(self):
        """Test creating a category."""
        category = models.Category.objects.create(title='electronic')
        self.assertEqual(str(category), category.title)

    def test_create_user_group(self):
        """Test creating a user group."""
        user1 = create_user(email='user1@example.com',password='password1')
        user2 = create_user(email='user2@example.com',password='password2')

        user_group = models.UserGroup.objects.create(sender=user1,receiver=user2,status='pending')

        self.assertEqual(str(user_group), user_group.status)