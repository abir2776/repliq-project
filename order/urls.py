from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path('orderItem-list/',views.OrderItemsAV.as_view(),name='orderItem_list'),
    path('order/',views.OrderAV.as_view(),name='order_create'),
]
