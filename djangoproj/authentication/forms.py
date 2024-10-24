from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=63,
        label="Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={"placeholder": "Nom d'utilisateur", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        max_length=63,
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Mot de passe", "class": "form-control"}
        ),
    )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Nom d'utilisateur"
        self.fields["username"].help_text = ""
        self.fields["username"].widget.attrs[
            "placeholder"
        ] = "Nom d'utilisateur"
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].error_messages[
            "unique"
        ] = "Ce nom d'utilisateur est déjà utilisé."

        self.fields["password1"].label = "Mot de passe"
        self.fields["password1"].help_text = (
            "- Votre mot de passe doit contenir au moins 8 caractères."
        )
        self.fields["password1"].widget.attrs["placeholder"] = "Mot de passe"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["aria-describedby"] = ""

        self.fields["password2"].label = "Confirmation de mot de passe"
        self.fields["password2"].help_text = ""
        self.fields["password2"].widget.attrs[
            "placeholder"
        ] = "Confirmer le mot de passe"
        self.fields["password2"].widget.attrs["class"] = "form-control"
