from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.credit_request, name='credit_request'),
    path('list/', views.credit_list, name='credit_list'),
    path('<int:credit_id>/detail/', views.credit_detail, name='credit_detail'),
]
