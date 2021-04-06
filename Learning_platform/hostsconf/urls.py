from django.conf.urls.static import static

from Learning_platform import settings
from academy_dashboard.urls import urlpatterns

urlpatterns = urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
