from rest_framework import serializers
from core import models

class OrederItemsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    shop = serializers.CharField(read_only=True)
    class Meta:
        model = models.OrderItems
        fields = ('user','shop','product','quantity')

class OrderSerializer(serializers.ModelSerializer):
    orderitem = serializers.PrimaryKeyRelatedField(queryset=models.OrderItems.objects.all(), many=True)
    shop = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    order_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Order
        fields = ('orderitem', 'shop', 'user', 'order_id')

    def create(self, validated_data):
        order_items = validated_data.pop('orderitem')
        order = models.Order.objects.create(**validated_data)
        for item in order_items:
            order.orderitem.add(item)
        return order