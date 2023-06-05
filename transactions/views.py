from django.shortcuts import render
from django.views import generic
from django.db.models import Sum

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
        # return Transaction.objects.order_by("date")[:25]


def upload(request):
    if request.method == "POST":
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

        statement = ofx.account.statement
        for t in statement.transactions:
            transaction = Transaction(
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

            # print({
            #     "payee": transaction.payee,
            #     "type": transaction.type,
            #     "date": transaction.date,
            #     "user_date": transaction.user_date,
            #     "amount": transaction.amount,
            #     "id": transaction.id,
            #     "memo": transaction.memo,
            #     "sic": transaction.sic,
            #     "mcc": transaction.mcc,
            #     "checknum": transaction.checknum
            # })

        # with codecs.open()
        # print(request.FILES)
        # form = UploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
        #     handle_uploaded_file(request.FILES["file"])
        #     return HttpResponseRedirect("/success/url/")
    else:
        pass

    return render(request, "transactions/upload.html", {})

    # question = get_object_or_404(Question, pk=question_id)
    # try:
    #     selected_choice = question.choice_set.get(pk=request.POST["choice"])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(
    #         request,
    #         "polls/detail.html",
    #         {
    #             "question": question,
    #             "error_message": "You didn't select a choice.",
    #         },
    #     )
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
