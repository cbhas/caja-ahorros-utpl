# managers.py
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y devuelve un usuario normal.
        """
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y devuelve un superusuario.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Asegurarse de que el superusuario tiene un 'username'
        if 'username' not in extra_fields:
            extra_fields['username'] = email.split('@')[0]

        return self.create_user(email, password, **extra_fields)
