"""
URL mappings for the user API.
"""
from django.urls import path

from user import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "user"

urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="create"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", views.ManagerUserView.as_view(), name="me"),
]
