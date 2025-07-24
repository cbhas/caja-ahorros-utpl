from django.db import models
from wallets.models import Wallet
from users.models import CustomUser


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("DEPOSIT", "Depósito"),
        ("WITHDRAWAL", "Retiro"),
        ("TRANSFER_SENT", "Transferencia enviada"),
        ("TRANSFER_RECEIVED", "Transferencia recibida"),
        ("PAYMENT", "Pago"),
        ("REFUND", "Reembolso"),
        ("CREDIT_DEPOSIT", "Depósito de crédito"),
        ("CREDIT_PAYMENT", "Pago de crédito"),
        # Nuevos tipos para objetivos de ahorro
        ("SAVINGS_DEPOSIT", "Depósito a objetivo de ahorro"),
        ("SAVINGS_WITHDRAWAL", "Retiro de objetivo de ahorro"),
        ("SAVINGS_RETURN", "Devolución de fondos de objetivo"),
        ("APORT","Aporte")
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pendiente"),
        ("COMPLETED", "Completada"),
        ("FAILED", "Fallida"),
        ("CANCELLED", "Cancelada"),
    ]

    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name="transactions"
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    recipient = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="received_transactions",
    )
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="COMPLETED"
    )
    reference_number = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "transactions"

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.reference_number}"
