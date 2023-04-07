"""
URL mappings for the user API.
"""
from django.urls import path

from user import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(),name='create'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/',views.ManagerUserView.as_view(),name='me'),
    path('user-list/', views.UserListView.as_view(), name='user_list'),
    path('usre-grp/<str:uid>/',views.UserGroupView.as_view(), name='user_grp'),
    path('grouping-requests/', views.UserGroupingRequests.as_view(), name='grouping_requests'),
]