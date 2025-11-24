from rest_framework.routers import DefaultRouter
from .views import ServiceCheckViewSet

router = DefaultRouter()
router.register(r"service-checks", ServiceCheckViewSet, basename="service-checks")

urlpatterns = router.urls