from django.conf.urls.static import static

from Learning_platform import settings
from academy_dashboard.urls import urlpatterns as courses_urlpatterns
from academy_forum.urls import urlpatterns as forum_urlpatterns

urlpatterns = courses_urlpatterns
urlpatterns += forum_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
