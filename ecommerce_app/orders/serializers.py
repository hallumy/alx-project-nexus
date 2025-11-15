from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = 'Cart'
        fields
