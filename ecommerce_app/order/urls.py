from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderItemViewSet, OrderViewSet, ShipmentViewSet

router = DefaultRouter()

router.register(r'order', OrderViewSet, basename='order')
router.register(r'orderitem', OrderItemViewSet, basename='orderitem')
router.register(r'shipment', ShipmentViewSet, basename='shipment')

urlpatterns = [
    path('', include(router.urls))
]