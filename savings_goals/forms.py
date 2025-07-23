from django import forms
from django.core.validators import MinValueValidator
from decimal import Decimal
from .models import SavingsGoal, SavingsTransaction


class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ["name", "category", "target_amount", "target_date"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre del objetivo"}
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "target_amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),
            "target_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }
        labels = {
            "name": "Nombre del objetivo",
            "category": "Categoría",
            "target_amount": "Meta ($)",
            "target_date": "Fecha objetivo",
        }

    def clean_target_amount(self):
        amount = self.cleaned_data["target_amount"]
        if amount <= 0:
            raise forms.ValidationError("La meta debe ser mayor a 0")
        return amount


class AddFundsForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "0.00",
                "step": "0.01",
                "min": "0.01",
            }
        ),
        label="Cantidad a agregar",
    )
    description = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Descripción (opcional)"}
        ),
        label="Descripción",
    )

    def __init__(self, *args, **kwargs):
        self.user_wallet = kwargs.pop("user_wallet", None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if self.user_wallet and amount > self.user_wallet.balance:
            raise forms.ValidationError("No tienes suficiente saldo en tu billetera")
        return amount


class WithdrawFundsForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "0.00",
                "step": "0.01",
                "min": "0.01",
            }
        ),
        label="Cantidad a retirar",
    )
    description = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Descripción (opcional)"}
        ),
        label="Descripción",
    )

    def __init__(self, *args, **kwargs):
        self.savings_goal = kwargs.pop("savings_goal", None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if self.savings_goal and amount > self.savings_goal.current_amount:
            raise forms.ValidationError("No hay suficientes fondos en este objetivo")
        return amount
