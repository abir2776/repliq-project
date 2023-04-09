"""Create views for categories."""
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from core import models
from . import serializers


class CategoryView(APIView):
    """View for getting category list and post a new category."""

    permission_classes = [permissions.IsAdminUser]
    serializer_classes = [serializers.CategorySerializer]

    def get(self, request):
        categories = models.Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    """View for getting a single category details. """

    permission_classes = [permissions.IsAdminUser]
    serializer_classes = [serializers.CategorySerializer]

    def get(self, request, uid):
        category = models.Category.objects.get(uid=uid)
        serializer = serializers.CategorySerializer(category)
        return Response(serializer.data)

    def delete(self, request, uid):
        category = models.Category.objects.get(uid=uid)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, uid):
        category = models.Category.objects.get(uid=uid)
        serializer = serializers.CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ShopListAV(APIView):
    """View for getting list of shops and posting a new shop."""

    perimission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Getting all shop and return list of shop."""
        shops = models.Shop.objects.filter(user=request.user)
        serializer = serializers.ShopSerializer(shops, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def post(self, request):
        """Post a new shop."""
        serializer = serializers.ShopSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data['user'] = request.user
            serializer.create(validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShopDetailAV(APIView):
    """View for getting a single item details."""

    perimission_classes = [permissions.IsAuthenticated]

    def get(self, request, uid):
        """Get a single item details."""
        shop = models.Shop.objects.get(uid=uid)
        serializer = serializers.ShopSerializer(shop)
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    def put(self, request, uid):
        """Update all details of shop."""
        shop = models.Shop.objects.get(uid=uid)
        serializer = serializers.ShopSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, uid):
        """Update some fields of shop."""
        shop = models.Shop.objects.get(uid=uid)
        serializer = serializers.ShopSerializer(shop, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, uid):
        """Delete a shop instance."""
        shop = models.Shop.objects.get(uid=uid)
        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def shop_login(request, uid):
    """Login to a shop."""
    shop = models.Shop.objects.get(uid=uid)
    shop.default = True
    shop.save()
    shops = models.Shop.objects.filter(uid__exact=uid).update(default=True)
    return Response(status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def shop_list(request):
    """Getting all the shops with the same category."""
    shop = models.Shop.objects.get(user=request.user, default=True)
    shops = models.Shop.objects.filter(category=shop.category)
    serializer = serializers.ShopSerializer(shops, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

