from django import forms
from django.forms import ModelForm

from .models import RecurringExpense


class RecurringExpenseForm(ModelForm):
    class Meta:
        model = RecurringExpense
        fields = ("particulars", "amount", "currency", "period", "active")
        widgets = {
            "particulars": forms.TextInput(attrs={"class": "form-control"}),
            "amount": forms.TextInput(attrs={"class": "form-control"}),
            "currency": forms.TextInput(attrs={"class": "form-control"}),
            "period": forms.NumberInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
