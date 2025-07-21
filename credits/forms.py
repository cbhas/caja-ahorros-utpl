from django import forms
from .models import Credit

class CreditRequestForm(forms.ModelForm):
    amount = forms.DecimalField(label='Monto del préstamo', max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'id': 'id_amount',
        'min': '100', 
        'max': '20000', 
        'step': '100'
    }))
    purpose = forms.CharField(label='Propósito del préstamo', max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ej: Educación, Viaje'
    }))

    class Meta:
        model = Credit
        fields = ['amount', 'term', 'purpose']
        widgets = {
            'term': forms.Select(attrs={'class': 'form-control', 'id': 'id_term'}),
        }