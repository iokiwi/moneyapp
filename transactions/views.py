from typing import Any, Dict
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.db.models import Sum, Count, Avg
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib import messages

# from django.utils.text import slugify

from ofxparse import OfxParser

from .models import Transaction, BankAccount


class IndexView(generic.TemplateView):
    template_name = "transactions/index.html"
    context_object_name = "transactions"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        transactions = Transaction.objects.all()
            # .filter(transaction_type="debit")

        if "payee" in self.request.GET:
            transactions = transactions.filter(payee=self.request.GET["payee"])

        if "transaction_type" in self.request.GET:
            transactions = transactions.filter(
                payee=self.request.GET["transaction_type"]
            )

        context["transactions"] = transactions.order_by("-date")
        context["transactions_total"] = transactions.aggregate(Sum("amount"))[
            "amount__sum"
        ]
        context["transactions_mean"] = transactions.aggregate(Avg("amount"))[
            "amount__avg"
        ]
        context["transactions_count"] = transactions.aggregate(Count("amount"))[
            "amount__count"
        ]

        return context


class StatsView(generic.ListView):
    template_name = "transactions/stats.html"
    context_object_name = "results"

    def get_queryset(self):
        return (
            Transaction.objects
            # .filter(transaction_type="debit")
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

        print(account)

        rows_imported = 0
        skipped_rows = 0
        for t in ofx.account.statement.transactions:
            try:
                transaction = Transaction(
                    account=account,
                    payee=t.payee,
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
                # print(transaction)
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

        # print(rows_imported, "/", len(ofx.account.statement.transactions))
        return HttpResponseRedirect(reverse("transactions:import"))
