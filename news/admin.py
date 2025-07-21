from django.contrib import admin
from .models import New

@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    list_display = ('title', 'place', 'date', 'created_at')
    list_filter = ('date', 'place')
    search_fields = ('title', 'content', 'place')
    readonly_fields = ('created_at',)
    date_hierarchy = 'date'
    fieldsets = (
        ('Información General', {
            'fields': ('title', 'content', 'image')
        }),
        ('Detalles de la noticia', {
            'fields': ('date', 'place')
        }),
        ('Auditoría', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
