from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email',
        'role', 'first_name', 'last_name',
    )
    list_editable = ('role',)
    search_fields = (
        'username', 'email', 'role',
        'first_name', 'last_name',
    )
    empty_value_display = '-пусто-'
