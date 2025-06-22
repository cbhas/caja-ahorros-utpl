# forms.py
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class CustomUserForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'password_confirm', 'document_type',
                  'document_number', 'phone']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        # Validación de contraseñas relajada (menos estricta)
        if len(password) < 6:  # Reducir a mínimo 6 caracteres
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")

        return cleaned_data

class CustomSuperUserCreationForm(UserCreationForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password_confirm']  # Solo email y password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data
