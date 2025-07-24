from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreditRequestForm
from .models import Credit
from wallets.models import Wallet
import math
from decimal import Decimal
from django.db.models import Sum, Count, Avg
from transactions.services import TransactionService

def credit_approve(request, credit_id):
    credit_request = get_object_or_404(Credit, id=credit_id)
    credit_request.status = 'approved'
    credit_request.save()

    main_wallet = Wallet.objects.filter(user__email="cda@utpl.edu.ec").first()
    
    TransactionService.create_transfer(
        sender_wallet=main_wallet,
        recipient_wallet=credit_request.wallet,
        amount=credit_request.amount,
        description=f"Desembolso de crédito (ID: {credit_request.id})"
    )

    return redirect('admin_credit_review', credit_id=credit_request.id)

def credit_reject(request, credit_id):
    credit_request = get_object_or_404(Credit, id=credit_id)
    credit_request.status = 'rejected'
    credit_request.save()
    return redirect('admin_credit_review', credit_id=credit_request.id)

@login_required
def credit_request(request):
    wallet = get_object_or_404(Wallet, user=request.user)

    if request.method == 'POST':
        form = CreditRequestForm(request.POST)
        if form.is_valid():
            credit = form.save(commit=False)
            credit.wallet = wallet
            
            amount = form.cleaned_data['amount'] # Already a Decimal
            term = form.cleaned_data['term']
            interest_rate = Decimal('12.00') # Convert to Decimal

            monthly_interest_rate = (interest_rate / Decimal('100')) / Decimal('12')
            
            # Perform calculations using Decimal for precision
            # Convert math.pow results to Decimal if they are floats
            numerator = amount * (monthly_interest_rate * Decimal(str(math.pow(1 + monthly_interest_rate, term))))
            denominator = Decimal(str(math.pow(1 + monthly_interest_rate, term))) - 1
            
            if denominator == 0:
                estimated_monthly_payment = Decimal('0.00') # Avoid division by zero
            else:
                estimated_monthly_payment = numerator / denominator

            credit.interest_rate = interest_rate
            credit.estimated_monthly_payment = estimated_monthly_payment
            credit.status = 'pending'
            credit.save()
            return redirect('credit_detail', credit_id=credit.id)
    else:
        form = CreditRequestForm()

    context = {
        'wallet': wallet,
        'form': form
    }
    return render(request, 'credits/credit_request.html', context)

@login_required
def credit_list(request):
    wallet = get_object_or_404(Wallet, user=request.user)
    credits = Credit.objects.filter(wallet=wallet).order_by('-created_at')
    context = {
        'credits': credits,
        'wallet': wallet
    }
    return render(request, 'credits/credit_list.html', context)

@login_required
def credit_detail(request, credit_id):
    credit = get_object_or_404(Credit, id=credit_id, wallet__user=request.user)
    context = {
        'credit': credit
    }
    return render(request, 'credits/credit_detail.html', context)


@login_required
def admin_credit_list(request):
    # Stats Cards
    approved_credits = Credit.objects.filter(status='approved')
    approved_count = approved_credits.count()
    approved_sum = approved_credits.aggregate(Sum('amount'))['amount__sum'] or 0

    # "En Revision" in the design seems to map to "pending" in the model
    pending_credits = Credit.objects.filter(status='pending')
    pending_count = pending_credits.count()
    pending_sum = pending_credits.aggregate(Sum('amount'))['amount__sum'] or 0

    # "Vencidos" in the design seems to map to "defaulted" in the model
    defaulted_credits = Credit.objects.filter(status='defaulted')
    defaulted_count = defaulted_credits.count()
    defaulted_sum = defaulted_credits.aggregate(Sum('amount'))['amount__sum'] or 0

    average_interest_rate = Credit.objects.aggregate(Avg('interest_rate'))['interest_rate__avg'] or 0

    # Solicitudes Pendientes
    # The design shows "Pendiente" and "En Revisión". We'll use our 'pending' status for this list.
    pending_applications = Credit.objects.filter(status='pending').order_by('-created_at')

    # Tipos de Crédito
    total_credits = Credit.objects.exclude(purpose__isnull=True).exclude(purpose__exact='').count()
    credit_type_distribution = Credit.objects.exclude(purpose__isnull=True).exclude(purpose__exact='').values('purpose').annotate(count=Count('purpose')).order_by('-count')

    credit_types_data = []
    if total_credits > 0:
        for item in credit_type_distribution:
            percentage = (item['count'] * 100) / total_credits
            credit_types_data.append({
                'purpose': item['purpose'],
                'count': item['count'],
                'percentage': round(percentage, 2)
            })

    context = {
        'approved_count': approved_count,
        'approved_sum': approved_sum,
        'pending_count': pending_count,
        'pending_sum': pending_sum,
        'defaulted_count': defaulted_count,
        'defaulted_sum': defaulted_sum,
        'average_interest_rate': average_interest_rate,
        'pending_applications': pending_applications,
        'credit_types_data': credit_types_data,
        'credits': Credit.objects.all(),
    }
    return render(request, 'credits/manage_credits.html', context)


@login_required
def admin_credit_review(request, credit_id):
    credit = get_object_or_404(Credit, id=credit_id)
    payments = credit.payments.all().order_by('-payment_date')
    context = {
        'credit': credit,
        'payments': payments,
    }
    return render(request, 'credits/admin_credit_review.html', context)
