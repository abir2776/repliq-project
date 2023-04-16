from rest_framework import serializers
from core import models


class CategorySerializer(serializers.Serializer):
    """Serializer for category.."""

    uid = serializers.CharField(read_only=True)
    title = serializers.CharField()

    def create(self, validated_data):
        return models.Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.save()
        return instance


class ShopSerializer(serializers.ModelSerializer):
    """Serializer for Shop."""

    uid = serializers.CharField(read_only=True)
    name = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all()
    )
    user = serializers.CharField(read_only=True)

    class Meta:
        model = models.Shop
        fields = ("uid", "name", "category", "user")


class GroupingSerializer(serializers.Serializer):
    """Serializer for grouping with one shop to another."""

    uid = serializers.CharField(read_only=True)
    sender = serializers.CharField(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=models.Shop.objects.all())
    status = serializers.CharField()

    def create(self, validated_data):
        return models.UserGroup.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.sender = validated_data.get('sender', instance.sender)
        # instance.receiver = validated_data.get('receiver', instance.receiver)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product..."""

    slug = serializers.CharField(read_only=True)
    image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True)
    shop = ShopSerializer(read_only=True)

    class Meta:
        model = models.Product
        fields = ("slug", "title", "price", "quantity", "shop", "image")
