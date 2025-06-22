# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomSuperUserCreationForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomSuperUserCreationForm

    model = CustomUser
    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()

    # Asegúrate de especificar solo los campos que están presentes en tu modelo
    # No agregues campos adicionales que no estén en el modelo `CustomUser`
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'document_type', 'document_number', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
