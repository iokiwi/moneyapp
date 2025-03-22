from typing import Any, Dict
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.views import generic
from django.views.generic.edit import FormView

from django.db.models import Sum, Count, Avg
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.functions import TruncWeek


from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from ofxparse import OfxParser

from .models import Transaction
from .forms import ImportForm

from bank_accounts.models import BankAccount


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "transactions/index.html"
    context_object_name = "transactions"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        transactions = Transaction.objects.all()

        if "payee" in self.request.GET:
            transactions = transactions.filter(payee=self.request.GET["payee"])

        if "transaction_type" in self.request.GET:
            transactions = transactions.filter(
                transaction_type=self.request.GET["transaction_type"]
            )
        if "account" in self.request.GET:
            transactions = transactions.filter(account__id=self.request.GET["account"])

        # Create a Paginator object with 25 items per page
        paginator = Paginator(transactions.order_by("-date"), 25)

        # Get the current page number from the request's GET parameters
        page_number = self.request.GET.get("page")

        # Get the Page object for the current page number
        page_obj = paginator.get_page(page_number)

        context["aggregate_stats"] = self.get_transaction_stats(transactions)
        context["debit_stats"] = self.get_transaction_stats(
            [t for t in transactions if t.amount < 0]
        )
        context["credit_stats"] = self.get_transaction_stats(
            [t for t in transactions if t.amount > 0]
        )

        # # Group transactions by week and annotate with weekly total and count
        # weekly_transactions = (
        #     transactions.annotate(week=TruncWeek("date"))
        #     .values("week")
        #     .annotate(total=Sum("amount"), count=Count("id"))
        #     .order_by("-week")
        # )
        # context["weekly_stats"] = self.get_weekly_transaction_stats(
        #   weekly_transactions)

        context["transactions"] = page_obj

        return context

    def get_weekly_transaction_stats(self, transactions):

        weekly_totals = [t["total"] for t in transactions]
        weekly_counts = [t["count"] for t in transactions]

        try:
            mean = sum(weekly_totals) / len(transactions)
        except ZeroDivisionError:
            mean = "N/A"

        return {
            "mean": mean,
            "count": sum(weekly_counts) / len(transactions),
        }

    def get_transaction_stats(self, transactions):
        if not transactions:
            return {"total": 0, "mean": 0, "count": 0}

        total = sum(t.amount for t in transactions)
        mean = total / len(transactions)
        count = len(transactions)
        return {"total": total, "mean": mean, "count": count}


def handle_uploaded_file(f):
    ofx = OfxParser.parse(f)

    try:
        account = BankAccount.objects.get(account_id=ofx.account.account_id)
    except BankAccount.DoesNotExist:
        account = BankAccount(
            account_id=ofx.account.account_id,
            account_type=ofx.account.account_type,
        )
        account.save()

    rows_imported = 0
    rows_failed = 0
    for t in ofx.account.statement.transactions:
        try:
            transaction = Transaction(
                account=account,
                payee=t.payee,
                payee_slug=slugify(t.payee),
                transaction_type=t.type,
                date=t.date,
                user_date=t.user_date,
                amount=t.amount,
                transaction_id=t.id,
                memo=t.memo,
                sic=t.sic,
                mcc=t.mcc,
                checknum=t.checknum,
            )
            transaction.save()
            rows_imported += 1
        except IntegrityError:
            rows_failed += 1

    rows_total = len(ofx.account.statement.transactions)

    return (rows_imported, rows_total, rows_failed)


class ImportView(LoginRequiredMixin, FormView):
    template_name = "transactions/import.html"
    form_class = ImportForm
    success_url = "/transactions/import"

    def form_valid(self, form):
        if form.is_valid():
            rows_imported, rows_total, rows_failed = handle_uploaded_file(
                self.request.FILES["file"]
            )
            message = "{}/{} transactions imported. {} duplicate transactions skipped."
            messages.success(
                self.request,
                message.format(rows_imported, rows_total, rows_failed),
            )
        else:
            messages.error(self.request, "No file uploaded")

        return HttpResponseRedirect(reverse("transactions:import"))
