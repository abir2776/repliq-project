from rest_framework import permissions, generics
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from core import models

from user.serializers import (
    UserSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    serializer_class = UserSerializer


class ManagerUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrive and return the authenticated user."""
        return self.request.user
