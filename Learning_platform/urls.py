from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import urls
from home_page import views

urls.handler404 = views.view_404
urls.handler500 = views.view_500
urls.handler403 = views.view_403
urls.handler400 = views.view_400

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('memberships/', include('memberships.urls')),
    path('courses/', include('courses.urls')),
    path('blog/', include('blog.urls')),
    path('forum/', include('forum.urls')),
    path('', include('home_page.urls')),
    path('', include('users.urls')),
    path('signal/', include('signal_app.urls')),
    path('copy_trade/', include('copy_trading.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
