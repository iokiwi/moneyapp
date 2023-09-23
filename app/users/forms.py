from django import forms
from django.core.mail import send_mail


class EmailLoginForm(forms.Form):
    email = forms.EmailField()

    def send_email(self, magic_link):
        send_mail(
            "Your magic login URL",
            magic_link,
            "noreply@localhost",
            [self.cleaned_data["email"]],
            fail_silently=False,
        )


class UserRegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()

    def send_email(self, magic_link):
        send_mail(
            "Your account signup URL",
            magic_link,
            "noreply@localhost",
            [self.cleaned_data["email"]],
            fail_silently=False,
        )
