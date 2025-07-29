from django.views.generic import ListView
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction
from wallets.models import Wallet


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "transactions/transaction_list.html"
    context_object_name = "transactions"

    def get_queryset(self):
        # Asegurar que el usuario tiene wallet
        wallet = Wallet.objects.filter(user=self.request.user).first()
        if wallet:
            return Transaction.objects.filter(wallet=wallet).order_by("-created_at")
        return Transaction.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.get_queryset()

        # Ingresos
        income = (
            transactions.filter(
                transaction_type__in=["DEPOSIT", "CREDIT_DEPOSIT", "APORT"],
                status="COMPLETED"
            ).aggregate(total=Sum("amount"))["total"] or 0
        )

        # Egresos
        expenses = (
            transactions.filter(
                transaction_type__in=[
                    "WITHDRAWAL",
                    "TRANSFER_SENT",
                    "PAYMENT",
                    "CREDIT_PAYMENT",
                    "SAVINGS_DEPOSIT",
                    "APORT",
                    "TRANSFER",
                ],
                status="COMPLETED",
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        # Obtener balance real del wallet
        wallet = Wallet.objects.filter(user=self.request.user).first()
        real_balance = wallet.balance if wallet else 0

        context["total_income"] = income
        context["total_expenses"] = expenses
        context["balance"] = real_balance  # Mostramos el real
        return context


@login_required
def transaction_list_admin(request):
    transacciones = Transaction.objects.select_related(
        "wallet__user", "recipient"
    ).order_by("-created_at")

    context = {
        "transacciones": transacciones,
    }
    return render(request, "transactions/transaction_list_admin.html", context)
