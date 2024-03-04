from django.contrib import admin
from django.urls import path, include  # Import the 'include' module

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("main.urls")),  # Include the unity_api URLs
    path("auth/", include("accounts.urls")),
]

# Add this for serving media files during development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
