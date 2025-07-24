from django.urls import path
from .views import *

urlpatterns = [
    path("", TransactionListView.as_view(), name="transaction_list"),
    path("admin/listar/", transaction_list_admin, name="transaction_list_admin"),
]
