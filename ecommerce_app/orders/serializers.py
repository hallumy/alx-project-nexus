from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = 'Cart'
        fields = ['id', 'user', 'created_at', 'updated_at']


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'variant', 'quantity', 'price', 'created_at', 'updated_at']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'order_number', 'total_amount',
                   'payment_status', 'order_date', 'shipped_date', 'payment_method']

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id','order','variant', 'quantity', 'price','subtotal']        
