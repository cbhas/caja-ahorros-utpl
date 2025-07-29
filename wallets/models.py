from django.db import models
from users.models import CustomUser

class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_credit_line = models.DecimalField(max_digits=10, decimal_places=2, default=2000)
    available_credit = models.DecimalField(max_digits=10, decimal_places=2, default=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet de {self.user.email}"

    def add_transaction(self, transaction_type, amount, description, recipient=None, status='COMPLETED'):
        """
        Método para agregar una transacción a esta billetera.
        """
        from transactions.models import Transaction
        from transactions.utils import generate_unique_reference  # ✅ importar la función

        transaction = Transaction.objects.create(
            wallet=self,
            transaction_type=transaction_type,
            amount=amount,
            description=description,
            recipient=recipient,
            status=status,
            reference_number=generate_unique_reference()  # ✅ campo único generado
        )
        return transaction


    def update_balance(self, amount, operation):
        """
        Actualiza el saldo de la billetera.
        - `operation`: 'add' para sumar, 'subtract' para restar.
        """
        if operation == 'add':
            self.balance += amount
        elif operation == 'subtract':
            if self.balance >= amount:
                self.balance -= amount
            else:
                raise ValueError("Saldo insuficiente.")
        self.save()
