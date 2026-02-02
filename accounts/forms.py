from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email scolastica")
    data_consent = forms.BooleanField(
        required=True,
        label="Acconsento al trattamento dei dati personali"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "class_group",
            "section",
            "school",
            "data_consent",
        )
