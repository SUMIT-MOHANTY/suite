from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import InvoiceViewSet, StatementViewSet

router = SimpleRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'statements', StatementViewSet, basename='statement')

urlpatterns = [
    path('api/', include(router.urls)),
]
