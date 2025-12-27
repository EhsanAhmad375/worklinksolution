"""
URL configuration for it_solutions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from website.views import custom_404
admin.site.site_header = "Worklink Coders"
admin.site.site_title = "Worklink Coders"
admin.site.index_title = "Welcome to Worklink Coders"
urlpatterns = [
    path('wlc/private/admin/', admin.site.urls),  # Django default admin
    path('admin-panel/', include('website.admin_urls')),  # Custom admin panel
    path('', include('website.urls')),
]

# Custom 404 handler
handler404 = custom_404

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
