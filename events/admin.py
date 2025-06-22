from django.contrib import admin

from django.contrib import admin

from events.models import Event


# Register your models here.
@admin.register(Event)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name',"date","cost")