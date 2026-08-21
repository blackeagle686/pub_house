from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('books/', include('apps.books.urls')),
    path('authors/', include('apps.authors.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('orders/', include('apps.orders.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('manuscripts/', include('apps.manuscripts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
