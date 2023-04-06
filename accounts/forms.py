from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class ChemMLUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name", "patronymic")


class ChemMLUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name", "patronymic")
