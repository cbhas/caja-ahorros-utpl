from django.urls import path
from .views import process_ticket_purchase

app_name = 'wallets'

urlpatterns = [
    path('purchase/<int:event_id>/', process_ticket_purchase, name='process_ticket_purchase'),
]