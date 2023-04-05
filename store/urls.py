"""URL mapping for category API."""
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('category-create/',views.CategoryView.as_view(),name='category-create'),
]
