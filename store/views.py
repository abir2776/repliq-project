"""Create views for categories."""
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from core import models
from . import serializers
from django.db.models import Q, F
from drf_spectacular.utils import extend_schema


class CategoryView(APIView):
    """View for getting category list and post a new category."""

    permission_classes = [permissions.IsAdminUser]
    serializer_classes = [serializers.CategorySerializer]

    def get(self, request):
        categories = models.Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    """View for getting a single category details."""

    permission_classes = [permissions.IsAdminUser]
    serializer_classes = [serializers.CategorySerializer]

    def get(self, request, uid):
        category = models.Category.objects.get(uid=uid)
        serializer = serializers.CategorySerializer(category)
        return Response(serializer.data)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
    def delete(self, request, uid):
        category = models.Category.objects.get(uid=uid)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
    def post(self, request):
        """Post a new shop."""
        serializer = serializers.ShopSerializer(data=request.data)
        if serializer.is_valid():
            models.Shop.objects.filter(user=request.user).update(default=False)
            validated_data = serializer.validated_data
            validated_data["user"] = request.user
            validated_data["default"] = True
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
    def put(self, request, uid):
        """Update all details of shop."""
        shop = models.Shop.objects.get(uid=uid)
        serializer = serializers.ShopSerializer(shop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
    def patch(self, request, uid):
        """Update some fields of shop."""
        shop = models.Shop.objects.get(uid=uid)
        serializer = serializers.ShopSerializer(shop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
    def delete(self, request, uid):
        """Delete a shop instance."""
        shop = models.Shop.objects.get(uid=uid)
        shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
@extend_schema(
    request=serializers.ProductSerializer,
    responses=serializers.ProductSerializer,
    # more customizations
)
def shop_login(request, uid):
    """Login to a shop."""
    request.user.shop_set.filter().update(default=False)
    shop = models.Shop.objects.get(uid=uid)
    shop.default = True
    shop.save()
    return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def shop_list(request):
    """Getting all the shops with the same category."""
    shop = models.Shop.objects.get(user=request.user, default=True)
    shops = models.Shop.objects.filter(category=shop.category)
    serializer = serializers.ShopSerializer(shops, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class GroupingRequestListAV(APIView):
    """View for listing all the request.."""

    perimission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Getting all the lists."""
        loged_in_shop = models.Shop.objects.get(user=request.user, default=True)
        requests = models.UserGroup.objects.filter(
            receiver=loged_in_shop, status="pending"
        )
        serializer = serializers.GroupingSerializer(requests, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
    def post(self, request):
        """Adding a request after sending."""
        serializer = serializers.GroupingSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data["sender"] = models.Shop.objects.get(
                user=request.user, default=True
            )
            validated_data["status"] = "pending"
            serializer.create(validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupingRequestDetailAV(APIView):
    """View for showing details.."""

    perimission_classes = [permissions.IsAuthenticated]

    def get(self, request, uid):
        """Get a single request detail."""
        G_request = models.UserGroup.objects.get(uid=uid)
        serializer = serializers.GroupingSerializer(G_request)

        return Response(serializer.data)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
    def patch(self, request, uid):
        """Update a request detail."""
        G_request = models.UserGroup.objects.get(uid=uid)
        serializer = serializers.GroupingSerializer(
            G_request, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
    def delete(self, request, uid):
        """Delete a request.."""
        G_request = models.UserGroup.objects.get(uid=uid)
        G_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyFriendListAV(APIView):
    """Get a list of connected shops."""

    def get(self, request):
        loged_in_shop = models.Shop.objects.get(user=request.user, default=True)
        groups = models.UserGroup.objects.filter(
            (Q(sender=loged_in_shop) | Q(receiver=loged_in_shop)) & Q(status="accepted")
        )
        shops = [
            group.sender if group.sender != loged_in_shop else group.receiver
            for group in groups
        ]
        serializer = serializers.ShopSerializer(shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyRequestsListAV(APIView):
    """Get list of requests send by logged in user."""

    def get(self, request):
        loged_in_shop = models.Shop.objects.get(user=request.user, default=True)
        groups = models.UserGroup.objects.filter(sender=loged_in_shop, status="pending")
        shops = [group.receiver for group in groups]
        serializer = serializers.ShopSerializer(shops, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductListAV(APIView):
    """API view for product list."""

    perimission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Showing all products of a shop."""
        loged_in_shop = models.Shop.objects.get(user=request.user, default=True)
        products = models.Product.objects.filter(shop=loged_in_shop)
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
    def post(self, request):
        """Creating a new product."""
        serializer = serializers.ProductSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data
            validated_data["shop"] = models.Shop.objects.get(
                user=request.user, default=True
            )
            serializer.create(validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAV(APIView):
    """Getting single product detail."""

    perimission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        """Get single product details."""
        product = models.Product.objects.get(slug=slug)
        serializer = serializers.ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
    def patch(self, request, slug):
        """Update single product detail."""
        product = models.Product.objects.get(slug=slug)
        serializer = serializers.ProductSerializer(
            product, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=serializers.ProductSerializer,
        responses=serializers.ProductSerializer,
        # more customizations
    )
    def delete(self, request, slug):
        """Delete a product.."""
        product = models.Product.objects.get(slug=slug)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FindProductAV(APIView):
    """Find all the product form friend shop.."""

    perimission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get the product form friend shop"""
        loged_in_shop = models.Shop.objects.get(user=request.user, default=True)
        groups = models.UserGroup.objects.filter(
            (Q(sender=loged_in_shop) | Q(receiver=loged_in_shop)) & Q(status="accepted")
        )
        shops = [
            group.sender if group.sender != loged_in_shop else group.receiver
            for group in groups
        ]
        product = models.Product.objects.filter(shop__in=shops)
        # groups = models.UserGroup.objects.filter(
        #     Q(sender=loged_in_shop) | Q(receiver=loged_in_shop),
        #     status='accepted'
        # )

        # product = models.Product.objects.filter(
        #     shop__in=groups.annotate(
        #         shop=F('sender') if F('sender') != loged_in_shop else F('receiver')
        #     ).values('shop')
        # )
        serializer = serializers.ProductSerializer(product, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
