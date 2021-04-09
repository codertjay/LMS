from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import urls
from home_page import views
from extensions.views import apple_pay_merchant_domain_association

urls.handler404 = views.view_404
urls.handler500 = views.view_500
urls.handler403 = views.view_403
urls.handler400 = views.view_400


WELL_KNOWN_URLS = [
    path(r'.well-known/apple-developer-merchantid-domain-association',
        apple_pay_merchant_domain_association, name='apple_pay_domain_association'),
]

urlpatterns = [
    path('admin-assassin-fx-url/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('memberships/', include('memberships.urls')),
    path('courses/', include('courses.urls')),
    path('blog/', include('blog.urls')),
    # path('academy_forum/', include('academy_forum.urls')),
    path('_coupon/', include('_coupon.urls')),
    path('', include('home_page.urls')),
    path('', include('users.urls')),
    path('signal/', include('signal_app.urls')),
    path('copy_trade/', include('copy_trading.urls')),
]
urlpatterns += WELL_KNOWN_URLS

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
