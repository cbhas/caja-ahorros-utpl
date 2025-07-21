from django.contrib import admin
from .models import AccountSettings

@admin.register(AccountSettings)
class AccountSettingsAdmin(admin.ModelAdmin):
    list_display = ('client', 'get_full_name', 'created_at', 'updated_at')
    search_fields = ('client__username', 'client__email', 'client__first_name', 'client__last_name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('client',)
        }),
        ('Biografía', {
            'fields': ('biography',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_full_name(self, obj):
        return f"{obj.client.first_name} {obj.client.last_name}"
    get_full_name.short_description = 'Nombre completo'

