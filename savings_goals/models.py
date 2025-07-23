from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from users.models import CustomUser

class SavingsGoal(models.Model):
    CATEGORY_CHOICES = [
        ('VACACIONES', 'Vacaciones'),
        ('AUTO', 'Nuevo auto'),
        ('EMERGENCIA', 'Fondo de emergencia'),
        ('CASA', 'Casa'),
        ('EDUCACION', 'Educación'),
        ('SALUD', 'Salud'),
        ('OTRO', 'Otro'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('COMPLETADO', 'Completado'),
        ('PAUSADO', 'Pausado'),
        ('CANCELADO', 'Cancelado'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='savings_goals')
    name = models.CharField(max_length=200, verbose_name="Nombre del objetivo")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Categoría")
    target_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Meta de ahorro"
    )
    current_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0'))],
        verbose_name="Cantidad actual"
    )
    target_date = models.DateField(verbose_name="Fecha objetivo")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'savings_goals'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.user.email}"

    @property
    def progress_percentage(self):
        """Calcula el porcentaje de progreso hacia la meta"""
        if self.target_amount > 0:
            return min(100, (float(self.current_amount) / float(self.target_amount)) * 100)
        return 0

    @property
    def remaining_amount(self):
        """Calcula la cantidad restante para alcanzar la meta"""
        return max(0, self.target_amount - self.current_amount)

    @property
    def is_completed(self):
        """Verifica si el objetivo ha sido completado"""
        return self.current_amount >= self.target_amount

    def add_funds(self, amount):
        """Agrega fondos al objetivo de ahorro"""
        if amount <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        self.current_amount += Decimal(str(amount))
        
        # Si alcanza o supera la meta, marca como completado
        if self.current_amount >= self.target_amount:
            self.status = 'COMPLETADO'
            self.current_amount = self.target_amount  # No permitir exceder la meta
        
        self.save()
        return self

    def withdraw_funds(self, amount):
        """Retira fondos del objetivo de ahorro"""
        if amount <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        
        if self.current_amount < amount:
            raise ValueError("Fondos insuficientes en el objetivo")
        
        self.current_amount -= Decimal(str(amount))
        
        # Si se retiran fondos y estaba completado, cambiar status a activo
        if self.status == 'COMPLETADO':
            self.status = 'ACTIVO'
        
        self.save()
        return self


class SavingsTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Depósito'),
        ('WITHDRAWAL', 'Retiro'),
    ]

    savings_goal = models.ForeignKey(
        SavingsGoal, 
        on_delete=models.CASCADE, 
        related_name='transactions'
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'savings_transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} - ${self.amount} - {self.savings_goal.name}"
    