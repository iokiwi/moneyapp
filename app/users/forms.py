from django import forms

# from django.urls import reverse


class EmailLoginForm(forms.Form):
    # Note(simonm): I don't like that this is hardcoded. However, using 'reverse'
    # here seems to result in a circular import.

    success_url = "/accounts/pending"

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        )
    )


class UserRegistrationForm(forms.Form):
    # Note(simonm): I don't like that this is hardcoded
    success_url = "/accounts/pending"

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "What should we call you?"}
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email Address"}
        )
    )
