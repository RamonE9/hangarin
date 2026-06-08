from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# ✅ REQUIRED for serviceworker fix
from django.views.static import serve
from django.views.decorators.cache import never_cache
from django.conf import settings
import os

urlpatterns = [
    path('admin/', admin.site.urls),

    # your existing routes
    path('', include('tasks.urls')),
    path('accounts/', include('allauth.urls')),

    # PWA routes
    path('', include('pwa.urls')),

    # ✅ OFFLINE PAGE
    path('offline/', lambda request: render(request, 'offline.html'), name='offline'),

    # ✅ SERVICE WORKER (CRITICAL FIX)
    path(
        'serviceworker.js',
        never_cache(serve),
        {
            'path': 'js/serviceworker.js',
            'document_root': os.path.join(settings.BASE_DIR, 'static'),
        },
    ),
]