from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChange, CustomUserCreation
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreation
    form = CustomUserChange
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active', 'is_applicant',)
    list_filter = ('email', 'is_staff', 'is_active', 'is_applicant',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)




admin.site.register(CustomUser, CustomUserAdmin)