from django.contrib import admin
from .models import Booking, FAQ

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['owner_name', 'dog_name', 'date_from', 'date_to', 'created_at']
    list_filter = ['date_from', 'date_to', 'created_at']
    search_fields = ['owner_name', 'dog_name', 'owner_email']
    readonly_fields = ['created_at']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order']
    list_editable = ['order']
    ordering = ['order']