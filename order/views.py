"""Views for order app."""
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from core import models
from . import serializers


class OrderItemsAV(APIView):
    """View for OrderItems."""
    perimission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        loged_in_shop = models.Shop.objects.get(user=request.user, default=True)
        orderitems = models.OrderItems.objects.filter(shop=loged_in_shop)
        serializer = serializers.OrederItemsSerializer(orderitems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.OrederItemsSerializer(data=request.data)
        loged_in_shop = models.Shop.objects.get(user=request.user, default=True)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data["user"] = request.user
            validated_data["shop"] = loged_in_shop
            serializer.create(validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class OrderAV(APIView):
    """View for place order."""
    perimission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        loged_in_shop = models.Shop.objects.get(user=request.user, default=True)
        order = models.Order.objects.get(shop=loged_in_shop)
        serializer = serializers.OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        loged_in_shop = models.Shop.objects.get(user=request.user, default=True)
        serializer = serializers.OrderSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data["user"] = request.user
            validated_data["shop"] = loged_in_shop
            order = serializer.create(validated_data)
            serializer = serializers.OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
