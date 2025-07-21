from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'document_type', 'document_number', 'phone',
        'is_active', 'is_verified', 'is_staff', 'date_joined'
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'preferred_currency', 'preferred_language')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'document_number')
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')

    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Información Personal', {
            'fields': (
                'username', 'first_name', 'last_name', 'phone',
                'document_type', 'document_number', 'address', 'profile_picture'
            )
        }),
        ('Preferencias', {
            'fields': ('preferred_currency', 'preferred_language', 'notification_preferences')
        }),
        ('Estado y Permisos', {
            'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Auditoría', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Cuenta', {
            'fields': ('account_balance',),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'password1', 'password2',
                'first_name', 'last_name', 'phone',
                'document_type', 'document_number'
            ),
        }),
    )

    ordering = ('-date_joined',)
