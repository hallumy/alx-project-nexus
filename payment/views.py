from rest_framework import viewsets
from .serializers import PaymentSerializer
from .models import Payment
from rest_framework.permissions import IsAuthenticated
from utils.mixins import AuthenticatedQuerysetMixin
from rest_framework.renderers import JSONRenderer

class PaymentViewSet(AuthenticatedQuerysetMixin, viewsets.ModelViewSet):
    """
    Provides CRUD operations for Payment objects via the API.
    Handles payment details, including mobile money transactions and statuses.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]