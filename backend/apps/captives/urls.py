from rest_framework.routers import DefaultRouter
from .views import CaptiveViewSet

app_name = 'captives'

router = DefaultRouter()
router.register(r'captives', CaptiveViewSet, basename='captive')

urlpatterns = router.urls
