from typing import Any, Dict
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify
from django.views import generic
from django.db.models import Sum, Count, Avg
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib import messages

# from django.utils.text import slugify

from ofxparse import OfxParser

from .models import Transaction
from bank_accounts.models import BankAccount


class IndexView(generic.TemplateView):
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

        context["aggregate_stats"] = self.get_transaction_stats(transactions)
        context["debit_stats"] = self.get_transaction_stats(
            [t for t in transactions if t.amount < 0]
        )
        context["credit_stats"] = self.get_transaction_stats(
            [t for t in transactions if t.amount > 0]
        )
        context["transactions"] = transactions.order_by("-date")

        return context

    def get_transaction_stats(self, transactions):
        if not transactions:
            return {"total": 0, "mean": 0, "count": 0}

        total = sum(t.amount for t in transactions)
        mean = total / len(transactions)
        count = len(transactions)
        return {"total": total, "mean": mean, "count": count}


class StatsView(generic.ListView):
    template_name = "transactions/stats.html"
    context_object_name = "results"

    def get_queryset(self):
        return (
            Transaction.objects.filter(transaction_type="debit")
            .values("payee")
            .annotate(
                total_amount=Sum("amount"),
                average_amount=Avg("amount"),
                transaction_count=Count("payee"),
            )
            .order_by("total_amount")
        )


def upload(request):
    if request.method == "GET":
        return render(request, "transactions/import.html", {})

    if request.method == "POST":
        if request.FILES.get("file") is None:
            messages.error(request, "No file uploaded")
            return HttpResponseRedirect(reverse("transactions:import"))

        ofx = OfxParser.parse(request.FILES["file"])

        try:
            account = BankAccount.objects.get(account_id=ofx.account.account_id)
        except BankAccount.DoesNotExist:
            account = BankAccount(
                account_id=ofx.account.account_id,
                account_type=ofx.account.account_type,
            )
            account.save()

        rows_imported = 0
        skipped_rows = 0
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
                skipped_rows += 1

        messages.success(
            request,
            "{}/{} transactions imported. {} duplicate transactions skipped.".format(
                rows_imported, len(ofx.account.statement.transactions), skipped_rows
            ),
        )

        return HttpResponseRedirect(reverse("transactions:import"))
