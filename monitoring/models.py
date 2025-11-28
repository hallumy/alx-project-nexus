from django.db import models

class ServiceCheck(models.Model):
    service_name = models.CharField(max_length=255)
    success = models.BooleanField()
    http_status_code = models.IntegerField(null=True, blank=True)
    response_time_ms = models.FloatField()
    checked_at = models.DateTimeField(auto_now_add=True)
    error = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.service_name} - {'Success' if self.success else 'Failed'}"