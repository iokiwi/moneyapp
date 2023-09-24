from django import forms


class EmailLoginForm(forms.Form):
    email = forms.EmailField()


class UserRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
