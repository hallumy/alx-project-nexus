import strawberry
from typing import Optional
from users.models import User, Address
from graphql_eco.graphql_types.user_types import UserType, AddressType


@strawberry.type
class UserMutation:

    # ✏ Update Profile
    @strawberry.mutation
    def update_profile(
        self,
        info,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> UserType:
        user = info.context["request"].user

        if not user.is_authenticated:
            raise Exception("Authentication required")

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.save()

        return UserType(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            is_admin=user.is_admin,
            is_vendor=user.is_vendor,
            is_customer=user.is_customer,
        )

    # ➕ Create Address
    @strawberry.mutation
    def create_address(
        self,
        info,
        street: str,
        city: str,
        region: str,
        country: str,
        postal_code: str,
        address_type: str,
    ) -> AddressType:
        user = info.context["request"].user

        if not user.is_authenticated:
            raise Exception("Authentication required")

        address = Address.objects.create(
            user=user,
            street=street,
            city=city,
            region=region,
            country=country,
            postal_code=postal_code,
            address_type=address_type,
        )

        return AddressType(
            id=address.id,
            street=address.street,
            city=address.city,
            region=address.region,
            country=address.country,
            postal_code=address.postal_code,
            address_type=address.address_type,
        )

    # ❌ Delete Address
    @strawberry.mutation
    def delete_address(self, info, address_id: int) -> bool:
        user = info.context["request"].user

        if not user.is_authenticated:
            raise Exception("Authentication required")

        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            return False

        address.delete()
        return True
