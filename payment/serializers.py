from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "payment_method",
            "amount",
            "phone_number",
            "transaction_id",
            "checkout_request_id",
            "result_code",
            "result_description",
            "payment_status",
            "paid_at",
            "payment_date",
        ]
        read_only_fields = [
            "transaction_id",
            "checkout_request_id",
            "result_code",
            "result_description",
            "payment_status",
            "paid_at",
            "payment_date",
        ]
