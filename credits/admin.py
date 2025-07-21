from django.contrib import admin
from .models import Credit, CreditPayment

class CreditPaymentInline(admin.TabularInline):
    model = CreditPayment
    extra = 0  # No extra empty forms

@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'amount', 'term', 'interest_rate', 'estimated_monthly_payment', 'status', 'created_at')
    list_filter = ('status', 'term', 'created_at')
    search_fields = ('wallet__user__email', 'purpose')
    inlines = [CreditPaymentInline] # To manage payments directly from the Credit admin page
    readonly_fields = ('created_at', 'updated_at', 'estimated_monthly_payment', 'interest_rate')

@admin.register(CreditPayment)
class CreditPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'credit', 'amount_paid', 'payment_date', 'reference_number')
    list_filter = ('payment_date',)
    search_fields = ('credit__id', 'reference_number')