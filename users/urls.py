from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, AddressViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from .auth_views import (
    RegisterAPIView, LoginAPIView, LogoutAPIView,
    JWTLoginAPIView, ProfileAPIView, JWTLogoutAPIView,
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register("address", AddressViewSet, basename='address')

urlpatterns = [
    path("", include(router.urls)),

    
    # Session-based auth
    path("auth/register/", RegisterAPIView.as_view()),
    path("auth/login/", LoginAPIView.as_view()),
    path("auth/logout/", LogoutAPIView.as_view()),
    path("auth/me/", ProfileAPIView.as_view()),

    # JWT-based auth
    path('auth/jwt/login/', TokenObtainPairView.as_view(), name='jwt-login'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    path('auth/jwt/logout/', JWTLogoutAPIView.as_view(), name='jwt-logout'),
]