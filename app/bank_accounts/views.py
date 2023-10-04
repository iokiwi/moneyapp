from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import BankAccount


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "bank_accounts/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bank_accounts"] = BankAccount.objects.all()
        return context


class DetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = "bank_accounts/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bank_accounts"] = BankAccount.objects.all()
        return context
