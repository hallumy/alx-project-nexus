from rest_framework import viewsets, filters
from .models import ServiceCheck
from .serializers import ServiceCheckSerializer
from rest_framework.renderers import JSONRenderer

class ServiceCheckViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceCheck.objects.all().order_by("-checked_at")
    serializer_class = ServiceCheckSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["checked_at","response_time_ms"]
    search_fields = ["service_name"]
    renderer_classes = [JSONRenderer]

