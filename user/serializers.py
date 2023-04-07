"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers

from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password':{'write_only':True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

        # validated_data['password'] = make_password(validated_data['password'])

        # return super().create(validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
    
class UserListSerializer(serializers.Serializer):
    """Serializer for showing user list."""
    uid = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

class UserGroupSerializer(serializers.Serializer):
    """Serializer for showing user grouping requests."""
    uid = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
