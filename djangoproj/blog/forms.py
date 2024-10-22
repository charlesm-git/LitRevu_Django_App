from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }


class ReviewForm(forms.ModelForm):

    class Meta:
        RATING_CHOICES = [
            (0, "0"),
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
        ]
        model = Review
        fields = ["headline", "rating", "body"]
        widgets = {
            "rating": forms.RadioSelect(choices=RATING_CHOICES),
            "headline": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }


class UsernameForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nom d'utilisateur",
                "class": "form-control centered-input",
            }
        ),
        label="",  # No label
        help_text="",  # No help text
    )
