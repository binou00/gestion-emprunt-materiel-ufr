from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ("email", "username", "first_name", "last_name", "role", "filiere", "niveau", "is_active")
    list_filter = ("role", "filiere", "niveau", "is_active", "is_staff")
    search_fields = ("email", "username", "first_name", "last_name", "telephone")
    ordering = ("last_name", "first_name")

    fieldsets = UserAdmin.fieldsets + (
        ("Informations UFR", {"fields": ("role", "filiere", "niveau", "telephone")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Informations UFR", {"fields": ("email", "role", "filiere", "niveau", "telephone")}),
    )
