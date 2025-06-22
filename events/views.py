from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from events.models import Event
from tickets.models import Ticket
from wallets.forms import TicketPurchaseForm

@login_required
def events_list_view(request):
    events = Event.objects.all()

    search_query = request.GET.get('search')  # Obtener el parámetro por el que busca

    if search_query:
        events = events.filter(
            Q(name__icontains=search_query))

    form = TicketPurchaseForm(user=request.user)

    return render(request, "events/events.html", {'events': events, 'form': form})


def event_purchase_modal(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    form = TicketPurchaseForm(user=request.user)

    return render(request, "events/includes/purchase_modal.html", {
        'event': event,
        'form': form
    })


@login_required
def my_tickets(request):
    # Obtener tickets agrupados por evento y contar cuántos hay de cada uno
    tickets = Ticket.objects.filter(user=request.user) \
        .values('event__name', 'event__date', 'event__place', 'event__image', 'cost') \
        .annotate(ticket_count=Count('event'))

    return render(request, 'events/my_tickets.html', {'tickets': tickets})