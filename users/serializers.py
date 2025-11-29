from .models import User, Address
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.

    Converts User model instances to JSON and validates input data for creating
    or updating users. Includes fields like username, email, role, phone, and address.
    """
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
)
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "role",
            "date_joined",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for the Address model"""

    class Meta:
        model = Address
        fields = [
            "id",
            "user",
            "street",
            "city",
            "region",
            "country",
            "postal_code",
            "postal_code",
        ]
        read_only_fields = ["user"]
