from rest_framework import viewsets
from .serializers import PaymentSerializer
from .models import Payment

class PaymentViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD operations for Payment objects via the API.
    Handles payment details, including mobile money transactions and statuses.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
