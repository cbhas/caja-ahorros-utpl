from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CreditRequestForm
from .models import Credit
from wallets.models import Wallet
import math
from decimal import Decimal

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