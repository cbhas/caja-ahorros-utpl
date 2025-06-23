"""
URL configuration for caja-ahorros-utpl project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from account_settings import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('home.urls')),
    path('account_settings/', include('account_settings.urls')),
    path('transactions/', include('transactions.urls')),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('events/', include('events.urls')),
    path('wallets/', include('wallets.urls', namespace='wallets')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
