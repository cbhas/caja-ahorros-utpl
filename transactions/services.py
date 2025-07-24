from decimal import Decimal
from django.db import transaction
from django.utils import timezone
import uuid
from .models import Transaction
from wallets.models import Wallet
from django.core.exceptions import ValidationError


class TransactionService:
    @staticmethod
    def generate_reference():
        return f"TRX-{uuid.uuid4().hex[:8].upper()}"

    @staticmethod
    def validate_amount(amount):
        if not isinstance(amount, (int, float, Decimal)):
            raise ValidationError("El monto debe ser un número")
        if amount <= 0:
            raise ValidationError("El monto debe ser mayor a 0")

    @classmethod
    def create_deposit(cls, wallet, amount, description="Depósito"):
        """Crear un depósito en la wallet"""
        cls.validate_amount(amount)

        with transaction.atomic():
            transaction_obj = Transaction.objects.create(
                wallet=wallet,
                transaction_type="DEPOSIT",
                amount=amount,
                description=description,
                reference_number=cls.generate_reference(),
                status="COMPLETED",
            )

            wallet.balance += Decimal(str(amount))
            wallet.save()

            return transaction_obj

    @classmethod
    def create_withdrawal(cls, wallet, amount, description="Retiro"):
        """Crear un retiro de la wallet"""
        cls.validate_amount(amount)

        if wallet.balance < amount:
            raise ValidationError("Saldo insuficiente")

        with transaction.atomic():
            transaction_obj = Transaction.objects.create(
                wallet=wallet,
                transaction_type="WITHDRAWAL",
                amount=-amount,
                description=description,
                reference_number=cls.generate_reference(),
                status="COMPLETED",
            )

            wallet.balance -= Decimal(str(amount))
            wallet.save()

            return transaction_obj

    @classmethod
    def create_transfer(
        cls, sender_wallet, recipient_wallet, amount, description="Transferencia"
    ):
        """Crear una transferencia entre wallets"""
        cls.validate_amount(amount)

        if sender_wallet.balance < amount:
            raise ValidationError("Saldo insuficiente")

        with transaction.atomic():
            reference = cls.generate_reference()

            # Transacción del emisor
            sender_transaction = Transaction.objects.create(
                wallet=sender_wallet,
                transaction_type="TRANSFER",
                amount=-amount,
                description=f"{description} enviada a {recipient_wallet.user.email}",
                reference_number=reference,
                recipient=recipient_wallet.user,
                status="COMPLETED",
            )

            # Transacción del receptor
            recipient_transaction = Transaction.objects.create(
                wallet=recipient_wallet,
                transaction_type="CREDIT_DEPOSIT",
                amount=amount,
                description=f"{description} recibida de {sender_wallet.user.first_name} {sender_wallet.user.last_name}",
                reference_number=f"RCV-{reference}",
                recipient=sender_wallet.user,
                status="COMPLETED",
            )

            # Actualizar balances
            sender_wallet.balance -= Decimal(str(amount))
            recipient_wallet.balance += Decimal(str(amount))
            sender_wallet.save()
            recipient_wallet.save()

            return sender_transaction, recipient_transaction
