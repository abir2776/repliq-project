from rest_framework import  permissions,generics
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import  permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from core import models

from user.serializers import (
    UserSerializer,
    UserListSerializer,
    UserGroupSerializer,
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
    
class UserListView(APIView):
    """Show the list of users by their category."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        users = get_user_model().objects.filter(category = self.request.user.category)
        serializer = UserListSerializer(users,many=True)
        return Response(serializer.data,status = status.HTTP_200_OK)
    
class UserGroupView(APIView):
    """Create and sow the list of user groups."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,uid):
        usergrp = models.UserGroup.objects.create(sender=self.request.user,receiver=get_user_model().objects.get(uid=uid),status='pending')
        data = {
            'sender':usergrp.sender.name,
            'receiver':usergrp.receiver.name,
            'status':usergrp.status

        }
        return Response(data=data, status=status.HTTP_201_CREATED)

class UserGroupingRequests(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = models.UserGroup.objects.filter(receiver=self.request.user,status='pending')
        serializer = UserGroupSerializer(users,many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)