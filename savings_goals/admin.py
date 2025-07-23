from django.contrib import admin
from .models import SavingsGoal, SavingsTransaction


@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "user",
        "category",
        "current_amount",
        "target_amount",
        "progress_percentage",
        "status",
        "target_date",
    ]
    list_filter = ["category", "status", "created_at"]
    search_fields = ["name", "user__email"]
    readonly_fields = ["progress_percentage", "created_at", "updated_at"]

    def progress_percentage(self, obj):
        return f"{obj.progress_percentage:.1f}%"

    progress_percentage.short_description = "Progreso"


@admin.register(SavingsTransaction)
class SavingsTransactionAdmin(admin.ModelAdmin):
    list_display = ["savings_goal", "transaction_type", "amount", "created_at"]
    list_filter = ["transaction_type", "created_at"]
    search_fields = ["savings_goal__name", "description"]
    readonly_fields = ["created_at"]
