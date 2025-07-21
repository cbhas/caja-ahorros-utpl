from django.contrib import admin
from .models import Wallet

from django.contrib import admin
from .models import Wallet

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_user_email', 'balance', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información de la Billetera', {
            'fields': ('user', 'balance')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.short_description = 'Correo del Usuario'
    get_user_email.admin_order_field = 'user__email'

    def has_add_permission(self, request):
        # Opcional: Deshabilita la creación de wallets desde el admin si lo prefieres
        return False

    def save_model(self, request, obj, form, change):
        if change and obj.balance < 0:
            raise ValueError("El saldo no puede ser negativo.")
        super().save_model(request, obj, form, change)

admin.site.register(Wallet, WalletAdmin)
