from django.db import models
from users.models import CustomUser

class AccountSettings(models.Model):
    client = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='account_settings')
    biography = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Configuración de la cuenta de {self.client.first_name} {self.client.last_name}"