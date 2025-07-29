from django import forms
from decimal import Decimal

class TransferForm(forms.Form):
    recipient_cedula = forms.CharField(
        min_length=10,
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Número de cédula del destinatario"
    )
    amount = forms.DecimalField(
        label="Monto a agregar",
        min_value=Decimal("0.01"),
        max_digits=10,
        decimal_places=2
    )

    description = forms.CharField(
        max_length=255,
        required=False,
        label="Descripción (opcional)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        label="Monto a depositar",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        max_length=255,
        required=False,
        label="Descripción (opcional)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


