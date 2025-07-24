from django.urls import path
from . import views
from .views import socio_list_view


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("admin/listar/", socio_list_view, name="socio_list"),
]
