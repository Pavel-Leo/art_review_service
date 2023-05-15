from django.contrib import admin

from reviews.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'bio',
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role')
    list_filter = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role')
    empty_value_display = '-пусто-'
