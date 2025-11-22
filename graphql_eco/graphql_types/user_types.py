import strawberry
from typing import List
from strawberry import django as strawberry_django
from users.models import User, Address

@strawberry_django.type(Address)
class AddressType:
    id: strawberry.ID
    street: str
    city: str
    region: str
    country: str
    postal_code: str
    address_type: str


@strawberry_django.type(User)
class UserType:
    id: strawberry.ID
    email: str
    first_name: str
    last_name: str
    role: str
    is_admin: bool
    is_vendor: bool
    is_customer: bool

    @strawberry.field
    def addresses(self) -> List[AddressType]:
        return list(self.address_set.all())
