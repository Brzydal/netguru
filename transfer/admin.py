from django.contrib import admin

from transfer.models import Transfer, UserAgent


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    list_display = ['id', 'picture', 'website', 'url_hash', 'correct_password_counter', 'created_by', 'is_valid']
    list_filter = ['created', 'modified', 'created_by']
    readonly_fields = ['picture', 'website', 'url_hash', 'correct_password_counter', 'created_by']


@admin.register(UserAgent)
class UserAgentAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_agent']
    readonly_fields = ['user', 'user_agent']
