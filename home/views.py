from django.contrib import messages
from django.shortcuts import render, redirect

from news.models import New
from transactions.models import Transaction
from wallets.models import Wallet
from django.db.models import Sum
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from transactions.forms import TransferForm
from users.models import CustomUser
from django.http import JsonResponse


from django.http import JsonResponse

@login_required
def dashboard_view(request):

    news = New.objects.all().order_by('-date')[:2]

    user = request.user
    current_balance = Wallet.objects.filter(user=user).first()

    if current_balance:
        today = now().date()
        daily_transactions = Transaction.objects.filter(wallet=current_balance, created_at__date=today)
        daily_income = daily_transactions.filter(transaction_type__in=['DEPOSIT']) \
                           .aggregate(total=Sum('amount'))['total'] or 0
        daily_expenses = daily_transactions.filter(transaction_type__in=['WITHDRAWAL', 'TRANSFER', 'TICKET_PURCHASE']) \
                             .aggregate(total=Sum('amount'))['total'] or 0

        recent_transactions = Transaction.objects.filter(
            wallet=current_balance
        ).order_by('-created_at')[:3]
    else:
        daily_income = 0
        daily_expenses = 0
        recent_transactions = []

    if request.method == "POST" and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = TransferForm(request.POST)
        if form.is_valid():
            recipient_cedula = form.cleaned_data['recipient_cedula']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']

            try:
                recipient = CustomUser.objects.get(document_number=recipient_cedula)
                recipient_wallet = Wallet.objects.filter(user=recipient).first()
            except CustomUser.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'El destinatario no existe.'})

            if current_balance.balance >= amount:
                transaction = Transaction.objects.create(
                    wallet=current_balance,
                    transaction_type='TRANSFER',
                    amount=amount,
                    recipient=recipient,
                    description=description,
                    reference_number="TRANS" + str(Transaction.objects.count() + 1),
                )

                current_balance.balance -= amount
                current_balance.save()

                Transaction.objects.create(
                    wallet=recipient_wallet,
                    transaction_type='DEPOSIT',
                    amount=amount,
                    recipient=user,
                    description=description,
                    reference_number="DEPO" + str(Transaction.objects.count() + 1),
                )

                recipient_wallet.balance += amount
                recipient_wallet.save()

                return JsonResponse({'success': True, 'message': f"Transferencia de ${amount} realizada con éxito a {recipient.first_name}."})
            else:
                return JsonResponse({'success': False, 'message': 'No tienes suficiente saldo para realizar esta transferencia.'})
        else:
            return JsonResponse({'success': False, 'message': 'Datos del formulario no válidos.'})

    else:
        form = TransferForm()

    context = {
        'client': user,
        'current_balance': current_balance,
        'daily_income': daily_income,
        'daily_expenses': daily_expenses,
        'form': form,
        'recent_transactions': recent_transactions,
        'news': news,
    }

    return render(request, 'home/home.html', context)


@login_required
def validate_account(request):
    if request.method == "POST":
        cedula = request.POST.get('cedula')
        if len(cedula) != 10:
            return JsonResponse({'valid': False, 'message': 'La cédula debe tener exactamente 10 dígitos.'})

        try:
            recipient = CustomUser.objects.get(document_number=cedula)
            return JsonResponse({
                'valid': True,
                'message': 'Cuenta válida.',
                'recipient': {
                    'name': recipient.first_name + ' ' + recipient.last_name,
                    'email': recipient.email
                }
            })
        except CustomUser.DoesNotExist:
            return JsonResponse({'valid': False, 'message': 'El destinatario no existe.'})
    return JsonResponse({'valid': False, 'message': 'Método no permitido.'})

def admin_dashboard_view(request):
    return render(request, "home/admin_home.html")