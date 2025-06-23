from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
import uuid

from tickets.models import Ticket
from transactions.models import Transaction
from .models import Wallet
from events.models import Event
from .forms import TransferForm, DepositForm, TicketPurchaseForm
from users.models import CustomUser


@login_required
def dashboard(request):
    wallet = Wallet.objects.get_or_create(user=request.user)[0]
    recent_transactions = Transaction.objects.filter(wallet=wallet)[:5]
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now()
    ).order_by('date')[:5]

    context = {
        'wallet': wallet,
        'recent_transactions': recent_transactions,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'wallet/dashboard.html', context)


@login_required
@transaction.atomic
def transfer_money(request):
    wallet = Wallet.objects.get(user=request.user)

    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient_email = form.cleaned_data['recipient_email']

            try:
                recipient = CustomUser.objects.get(email=recipient_email)
                recipient_wallet = Wallet.objects.get_or_create(user=recipient)[0]

                if wallet.balance >= amount:
                    # Create transfer transaction
                    reference = f"TRF-{uuid.uuid4().hex[:8]}"

                    Transaction.objects.create(
                        wallet=wallet,
                        transaction_type='TRANSFER',
                        amount=-amount,
                        recipient=recipient,
                        description=f"Transferencia a {recipient_email}",
                    )

                    Transaction.objects.create(
                        wallet=recipient_wallet,
                        transaction_type='TRANSFER',
                        amount=amount,
                        recipient=request.user,
                        description=f"Transferencia de {request.user.username}",
                        reference_number=f"RCV-{reference}"
                    )

                    wallet.balance -= amount
                    recipient_wallet.balance += amount
                    wallet.save()
                    recipient_wallet.save()

                    messages.success(request, 'Transferencia realizada con éxito')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Saldo insuficiente')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Usuario no encontrado')
    else:
        form = TransferForm()

    return render(request, 'wallet/transfer.html', {'form': form})


@login_required
def process_ticket_purchase(request, event_id):
    if request.method != 'POST':
        return redirect('events_list')

    event = get_object_or_404(Event, pk=event_id)
    form = TicketPurchaseForm(request.user, request.POST)

    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        wallet = form.cleaned_data['wallet']
        total_cost = event.cost * quantity

        recipient = CustomUser.objects.get(email="caja-ahorros-utpl@gmail.com")
        recipient_wallet = Wallet.objects.get(user=recipient)

        if wallet.balance < total_cost:
            messages.error(request, 'No tienes suficientes fondos.')
        elif event.available_tickets < quantity:
            messages.error(request, 'No hay suficientes tickets disponibles')
        else:
            with transaction.atomic():
                # Create tickets
                for _ in range(quantity):
                    Ticket.objects.create(
                        event=event,
                        user=request.user,
                        cost=event.cost,
                    )

                # Create transaction
                Transaction.objects.create(
                    wallet=wallet,
                    transaction_type='TICKET_PURCHASE',
                    amount=total_cost,
                    description=f"Compra de {quantity} ticket(s) para {event.name}",
                    recipient=recipient,
                    reference_number=f"EVT-{uuid.uuid4().hex[:8]}"
                )

                # Update wallet and event
                wallet.balance -= total_cost
                wallet.save()
                recipient_wallet.balance += total_cost
                recipient_wallet.save()
                event.available_tickets -= quantity
                event.save()

                messages.success(request, 'Compra Completada')
                return redirect('events_list')

    # If there are errors, return to modal with errors
    return render(request, "events/events.html", {
        'event': event,
        'form': form
    })