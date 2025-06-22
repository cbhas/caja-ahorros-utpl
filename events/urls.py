from django.urls import path
from .views import events_list_view, event_purchase_modal, my_tickets

urlpatterns = [
    path('', events_list_view, name='events_list'),
    path('purchase/<int:event_id>/', event_purchase_modal, name='event_purchase_modal'),
    path('my-tickets/', my_tickets, name='my_tickets'),
]
