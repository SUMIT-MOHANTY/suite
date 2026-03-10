from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.auth.urls')),
    path('api/captives/', include('apps.captives.urls')),
    path('api/policies/', include('apps.policies.urls')),
    path('api/claims/', include('apps.claims.urls')),
    path('api/contacts/', include('apps.contacts.urls')),
    path('api/financials/', include('apps.financials.urls')),
]
