from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.credit_request, name='credit_request'),
    path('list/', views.credit_list, name='credit_list'),
    path('<int:credit_id>/detail/', views.credit_detail, name='credit_detail'),
    path('admin/', views.admin_credit_list, name='admin_credits'),
    path('admin/review/<int:credit_id>/', views.admin_credit_review, name='admin_credit_review'),
    path('approve/<int:credit_id>/', views.credit_approve, name='credit_approve'),
]
