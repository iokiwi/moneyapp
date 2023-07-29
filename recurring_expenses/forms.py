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
