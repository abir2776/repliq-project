from rest_framework import serializers
from core import models


class CategorySerializer(serializers.Serializer):
    """Serializer for category.."""
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()

    def create(self, validated_data):
        return models.Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.save()
        return instance
    
class ShopSerializer(serializers.Serializer):
    """Serializer for Shop."""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    category = serializers.PrimaryKeyRelatedField(queryset=models.Category.objects.all())

    def create(self, validated_data):
        return models.Shop.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.category = validated_data.get('category',instance.category)
        instance.save()
        return instance


