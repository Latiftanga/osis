from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'password', 'school')}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_student',
            'is_parent',
            'is_teacher',
            'is_staff',
            'is_superuser'
        )}),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'school')
        }),
    )


admin.site.register(models.School)
admin.site.register(models.User)
admin.site.register(models.Programme)
admin.site.register(models.Grade)