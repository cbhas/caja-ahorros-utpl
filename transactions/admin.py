from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'reference_number',
        'transaction_type',
        'wallet',
        'get_wallet_owner',
        'amount',
        'status',
        'created_at',
    )
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = (
        'reference_number',
        'description',
        'wallet__user__username',
        'recipient__username',
        'recipient__email'
    )
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información de la Transacción', {
            'fields': (
                'wallet',
                'transaction_type',
                'amount',
                'recipient',
                'description',
                'status',
                'reference_number',
            )
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'created_at'

    def get_wallet_owner(self, obj):
        return obj.wallet.user.get_full_name() if obj.wallet and obj.wallet.user else 'N/A'
    get_wallet_owner.short_description = 'Dueño del Monedero'
    get_wallet_owner.admin_order_field = 'wallet__user__first_name'
