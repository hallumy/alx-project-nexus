class AuthenticatedQuerysetMixin:
    """
    Mixin to safely filter querysets by the authenticated user
    and prevent Swagger (drf_yasg) schema generation errors.
    """

    user_field = "user"

    def get_queryset(self):
        user = getattr(self.request, "user", None)

        if (
            not user
            or not user.is_authenticated
            or getattr(self, "swagger_fake_view", False)
        ):
            return self.queryset.none()

        filter_kwargs = {self.user_field: user}
        return self.queryset.filter(**filter_kwargs)
