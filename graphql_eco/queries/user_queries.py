import strawberry
from typing import List, Optional
from users.models import User, Address
from graphql_eco.graphql_types.user_types import UserType, AddressType


@strawberry.type
class UserQuery:

    @strawberry.field
    def users(self, info) -> List[UserType]:
        request = info.context["request"]
        user = request.user

        if not user.is_authenticated:
            return []

        if user.is_admin:
            qs = User.objects.all()

        elif user.is_vendor:
            qs = User.objects.filter(role=User.Roles.CUSTOMER)

        else:
            qs = User.objects.filter(id=user.id)

        return [
            UserType(
                id=u.id,
                email=u.email,
                first_name=u.first_name,
                last_name=u.last_name,
                role=u.role,
                is_admin=u.is_admin,
                is_vendor=u.is_vendor,
                is_customer=u.is_customer,
            )
            for u in qs
        ]

    # SINGLE USER
    @strawberry.field
    def user(self, info, user_id: int) -> Optional[UserType]:
        request = info.context["request"]
        user = request.user

        if not user.is_authenticated:
            return None

        try:
            target = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

        # Permissions
        if not user.is_admin and target != user:
            return None

        return UserType(
            id=target.id,
            email=target.email,
            first_name=target.first_name,
            last_name=target.last_name,
            role=target.role,
            is_admin=target.is_admin,
            is_vendor=target.is_vendor,
            is_customer=target.is_customer,
        )

    @strawberry.field
    def addresses(self, info) -> List[AddressType]:
        request = info.context["request"]
        user = request.user

        if not user.is_authenticated:
            return []

        qs = Address.objects.filter(user=user)

        return [
            AddressType(
                id=a.id,
                street=a.street,
                city=a.city,
                region=a.region,
                country=a.country,
                postal_code=a.postal_code,
                address_type=a.address_type,
            )
            for a in qs
        ]

    #  SINGLE ADDRESS
    @strawberry.field
    def address(self, info, address_id: int) -> Optional[AddressType]:
        request = info.context["request"]
        user = request.user

        if not user.is_authenticated:
            return None

        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            return None

        return AddressType(
            id=address.id,
            street=address.street,
            city=address.city,
            region=address.region,
            country=address.country,
            postal_code=address.postal_code,
            address_type=address.address_type,
        )
