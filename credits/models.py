from django.db import models
from wallets.models import Wallet

class Credit(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('approved', 'Aprobado'),
        ('rejected', 'Rechazado'),
        ('active', 'Activo'),
        ('paid', 'Pagado'),
        ('defaulted', 'Incumplido'),
    )

    TERM_CHOICES = (
        (12, '12 meses'),
        (24, '24 meses'),
        (36, '36 meses'),
        (48, '48 meses'),
    )

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='credits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term = models.IntegerField(choices=TERM_CHOICES)  # Plazo en meses
    purpose = models.CharField(max_length=255, blank=True, null=True)
    estimated_monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Credit for {self.wallet.user.email} - {self.amount}"

class CreditPayment(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Payment for Credit {self.credit.id} - {self.amount_paid}"