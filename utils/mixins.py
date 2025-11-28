from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
import hashlib
import json


class CachedQuerysetMixin:
    """
    Centralized caching + filtering + ordering for DRF viewsets.
    Works for all list endpoints.
    """

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    cache_timeout = 60 * 5 
    cache_prefix = None   
    filterset_fields = []   
    ordering_fields = "__all__" 
    ordering = None

    def generate_cache_key(self, request):
        params = request.query_params.dict()
        raw = json.dumps(params, sort_keys=True)
        hashed = hashlib.md5(raw.encode()).hexdigest()

        prefix = self.cache_prefix or self.__class__.__name__.lower()
        return f"{prefix}:{hashed}"

    def list(self, request, *args, **kwargs):
        """
        Override list() to apply caching automatically.
        """
        cache_key = self.generate_cache_key(request)
        cached = cache.get(cache_key)

        if cached:
            return cached

        response = super().list(request, *args, **kwargs)
        if hasattr(response, "render") and callable(response.render):
            response.render()

        cache.set(cache_key, response, self.cache_timeout)

        return response
    
class AuthenticatedQuerysetMixin:
    """
    Mixin to safely filter querysets by the authenticated user
    and prevent Swagger (drf_yasg) schema generation errors.
    """

    user_field = "user"

    def get_queryset(self):
        user = getattr(self.request, "user", None)

        if (
            not user
            or not user.is_authenticated
            or getattr(self, "swagger_fake_view", False)
        ):
            return self.queryset.none()

        filter_kwargs = {self.user_field: user}
        return self.queryset.filter(**filter_kwargs)
