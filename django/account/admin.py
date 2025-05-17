from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account import models

@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    model = models.User
    list_display = ("email", "name", "icon_code", "is_staff", "is_active", "familygroup")
    list_filter = ("is_staff", "is_active", "familygroup")
    fieldsets = (
        (None, {"fields": ("email", "password", "name", "icon_code", "familygroup")}),
        ("権限", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2", "icon_code", "familygroup", "is_staff", "is_active")}
        ),
    )
    search_fields = ("email", "name")
    ordering = ("email",)

admin.site.register(models.FamilyGroup)