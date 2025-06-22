from django.views.generic import ListView
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        return Transaction.objects.filter(wallet=self.request.user.wallet)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.get_queryset()

        # Calcular ingresos totales (depósitos y transferencias recibidas)
        income = transactions.filter(
            transaction_type__in=['DEPOSIT', 'TRANSFER'],
            status='COMPLETED'
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Calcular gastos totales (retiros y transferencias enviadas)
        expenses = transactions.filter(
            transaction_type__in=['WITHDRAWAL', 'TRANSFER', 'TICKET_PURCHASE'],
            status='COMPLETED'
        ).aggregate(total=Sum('amount'))['total'] or 0

        context['total_income'] = income
        context['total_expenses'] = expenses
        context['balance'] = income - expenses
        return context
