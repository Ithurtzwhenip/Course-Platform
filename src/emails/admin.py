from django.contrib import admin
from .models import Email, EmailVerificationEvent

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'timestamp')
    search_fields = ('email',)

@admin.register(EmailVerificationEvent)
class EmailVerificationEventAdmin(admin.ModelAdmin):
    list_display = ('email', 'attempts', 'expired', 'timestamp')
    search_fields = ('email',)
    list_filter = ('expired',)
