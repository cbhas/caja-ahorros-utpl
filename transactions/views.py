from django.views.generic import ListView
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from transactions.models import Transaction


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transactions/transaction_list.html"
    context_object_name = "transactions"

    def get_queryset(self):
        return Transaction.objects.filter(wallet=self.request.user.wallet)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.get_queryset()

        # Calcular ingresos totales (depósitos y transferencias recibidas)
<<<<<<< Updated upstream
        income = transactions.filter(
            transaction_type__in=['DEPOSIT', 'TRANSFER','CREDIT_DEPOSIT'],
            status='COMPLETED'
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Calcular gastos totales (retiros y transferencias enviadas)
        expenses = transactions.filter(
            transaction_type__in=['WITHDRAWAL', 'TRANSFER', 'TICKET_PURCHASE','CREDIT_PAYMENT'],
            status='COMPLETED'
        ).aggregate(total=Sum('amount'))['total'] or 0

=======
        income = (
            transactions.filter(
                transaction_type__in=["DEPOSIT", "TRANSFER", "CREDIT_DEPOSIT"],
                status="COMPLETED",
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        # Calcular gastos totales (retiros y transferencias enviadas)
        expenses = (
            transactions.filter(
                transaction_type__in=[
                    "WITHDRAWAL",
                    "TRANSFER",
                    "TICKET_PURCHASE",
                    "CREDIT_PAYMENT",
                ],
                status="COMPLETED",
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )
>>>>>>> Stashed changes

        context["total_income"] = income
        context["total_expenses"] = expenses
        context["balance"] = income - expenses
        return context


@login_required
def transaction_list_admin(request):
    # Obtener todas las transacciones, con los usuarios relacionados
    transacciones = Transaction.objects.select_related(
        "wallet__user", "recipient"
    ).order_by("-created_at")

    context = {
        "transacciones": transacciones,
    }

    return render(request, "transactions/transaction_list_admin.html", context)