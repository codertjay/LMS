from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blog.views import BlogCreateView
from courses.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('create_post/', BlogCreateView.as_view(), name='create_post'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('memberships/', include('memberships.urls')),
    path('courses/', include('courses.urls')),
    path('blog/', include('blog.urls')),
    path('', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
