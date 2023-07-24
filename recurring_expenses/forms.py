from django import forms
from django.forms import ModelForm

from .models import RecurringExpense


class RecurringExpenseForm(ModelForm):
    class Meta:
        model = RecurringExpense
        fields = ("particulars", "amount", "currency", "period", "active")
        widgets = {
            "particulars": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Netflix"}
            ),
            "amount": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "24.99"}
            ),
            "currency": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "NZD"}
            ),
            "period": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "1"}
            ),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    # particulars = forms.CharField(
    #     required=True,
    #     max_length=256,
    #     widget=forms.TextInput(
    #         attrs={"class": "form-control", "placeholder": "Netflix"}
    #     ),
    # )

    # amount = forms.DecimalField(
    #     required=True,
    #     max_digits=10,
    #     decimal_places=2,
    #     widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "24.99"}),
    # )

    # currency = forms.CharField(
    #     required=True,
    #     initial="NZD",
    #     max_length=3,
    #     widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "NZD"}),
    # )

    # period = forms.IntegerField(
    #     required=True,
    #     initial=1,
    #     widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "1"})
    # )

    # active = forms.BooleanField(
    #     initial=True, widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    # )
