from django.contrib import admin

from transfer.models import Transfer


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    pass
