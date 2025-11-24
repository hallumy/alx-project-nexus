from rest_framework import serializers
from .models import ServiceCheck

class ServiceCheckSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id","service_name","success","http_status_code","response_time_ms","checked_at"]
        read_only_fields = ["id","checked_at"]