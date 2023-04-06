from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import ChemMLUserChangeForm, ChemMLUserCreationForm 

ChemMLUser = get_user_model()


@admin.register(ChemMLUser)
class ChemMLUserAdmin(UserAdmin):
    add_form = ChemMLUserCreationForm
    form = ChemMLUserChangeForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональная информация",
            {"fields": ("first_name", "last_name", "patronymic", "username")},
        ),
        (
            "Доступы",
            {
                "fields": (
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "patronymic",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    model = ChemMLUser 
    list_display = [
        "email",
        "first_name",
        "last_name",
        "patronymic",
        "is_superuser",
    ]
