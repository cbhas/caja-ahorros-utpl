from django.urls import path
from . import views
from .views import validate_account

urlpatterns = [
    path('', views.dashboard_view, name='home'),
    path('validate_account/', validate_account, name='validate_account'),
]
