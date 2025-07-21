# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager  # Importar el manager personalizado

class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre de usuario",
        null=True,
        blank=True  # Permite que sea opcional para los usuarios normales
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    document_type = models.CharField(max_length=20, choices=[
        ('CEDULA', 'CEDULA'),
        ('RUC', 'RUC'),
        ('PASSPORT', 'Pasaporte')
    ])
    document_number = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)
    preferred_currency = models.CharField(max_length=3, default='USD')
    preferred_language = models.CharField(max_length=2, default='es')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'  # El email sigue siendo el identificador único
    REQUIRED_FIELDS = ['username']  # Hacer que username sea requerido para superusuarios

    objects = CustomUserManager()  # Asignar el manager personalizado

    class Meta:
        db_table = 'custom_users'

    def __str__(self):
        return self.email
