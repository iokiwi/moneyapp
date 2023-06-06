from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib import messages

from ofxparse import OfxParser

from .models import Transaction

# class AccountsIndexView(generic.ListView):
#     pass

class IndexView(generic.ListView):
    template_name = "transactions/index.html"
    context_object_name = "transactions"

    def get_queryset(self):
        return Transaction.objects.order_by("date")[:25]


class StatsView(generic.ListView):
    template_name = "transactions/stats.html"
    context_object_name = "results"

    def get_queryset(self):
        return Transaction.objects.values('payee').annotate(total_amount=Sum('amount')).order_by('total_amount')


def upload(request):

    if request.method == "GET":
        return render(request, "transactions/upload.html", {})

    if request.method == "POST":
        if request.FILES.get("file") is None:
            messages.error(request, "No file uploaded")
            return HttpResponseRedirect(reverse("transactions:upload"))

        ofx = OfxParser.parse(request.FILES["file"])

        account = ofx.account
        print({
            "account_id": account.account_id,
            "account_type": account.account_type,
            "branch_id": account.branch_id,
            "curdef": account.curdef,
            "institution": account.institution,
            "number": account.number,
            "routing_number": account.routing_number,
            #  ,"statement": account.statement
            "type": account.type,
            "warnings": account.warnings,
        })

        rows_imported = 0
        duplicate_rows = 0
        for t in ofx.account.statement.transactions:
            try:
                transaction = Transaction(
                    # TODO(simonm): Link transaction to bank account
                    payee=t.payee,
                    transaction_type=t.type,
                    date=t.date,
                    user_date=t.user_date,
                    amount=t.amount,
                    transaction_id=t.id,
                    memo=t.memo,
                    sic=t.sic,
                    mcc=t.mcc,
                    checknum=t.checknum
                )
                transaction.save()
                rows_imported += 1
            except IntegrityError as e:
                duplicate_rows += 1
                # pass

        messages.success(request, "{}/{} transactions imported. {} duplicate transactions skipped.".format(
            rows_imported, len(account.statement.transactions), duplicate_rows))

        # print(rows_imported, "/", len(ofx.account.statement.transactions))
        return HttpResponseRedirect(reverse("transactions:upload"))
