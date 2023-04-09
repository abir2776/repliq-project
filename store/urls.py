"""URL mapping for category API."""
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('category-list/', views.CategoryView.as_view(), name='category_list'),
    path(
        
        'category-detail/<str:uid>/',
        views.CategoryDetailView.as_view(),
        name='category_detail',
    ),
    path('shop-list/',views.ShopListAV.as_view(), name='shop_list'),
    path('shop-detail/<str:uid>/', views.ShopDetailAV.as_view(), name='shop_detail'),
    path('find-shop/', views.shop_list, name='find_shop'),
    path('login-shop/<str:uid>/', views.shop_login, name='shop_login'),
]
