from django import forms
from django.core.validators import MinValueValidator
from wallets.models import Wallet

class TransferForm(forms.Form):
    recipient_cedula = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label="Monto a transferir"
    )
    description = forms.CharField(
        max_length=255,
        required=False,
        label="Descripción (opcional)"
    )

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label="Monto a depositar"
    )
    description = forms.CharField(
        max_length=255,
        required=False,
        label="Descripción (opcional)"
    )

class TicketPurchaseForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control text-center',
            'id': 'cantidad'
        })
    )

    wallet = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'pago'
        })
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['wallet'].queryset = Wallet.objects.filter(user=user)
            self.fields['wallet'].label_from_instance = lambda obj: f"{obj.user.email} - Balance: ${obj.balance}"