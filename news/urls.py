from django.urls import path
from .views import news_list_view

urlpatterns = [
    path('', news_list_view, name='news_list'),
]
