from django.contrib import admin
from .models import Wallet

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_at', 'updated_at')  # Campos visibles en la lista
    list_filter = ('created_at', 'updated_at')  # Filtros en el lateral
    search_fields = ('user__email',)  # Habilitar búsqueda por email del usuario
    readonly_fields = ('created_at', 'updated_at')  # Campos que no se pueden editar
    fieldsets = (
        (None, {
            'fields': ('user', 'balance')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


    def has_add_permission(self, request):
        # Opcional: Deshabilita la creación de wallets desde el admin si lo prefieres
        return False

    def save_model(self, request, obj, form, change):
        if change and obj.balance < 0:
            raise ValueError("El saldo no puede ser negativo.")
        super().save_model(request, obj, form, change)

admin.site.register(Wallet, WalletAdmin)
