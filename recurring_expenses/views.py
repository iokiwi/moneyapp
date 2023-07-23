from django.shortcuts import render
from django.views import generic
from .models import RecurringExpense

from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render
from django.contrib import messages

from django.urls import reverse


class IndexView(generic.TemplateView):

    template_name = "recurring_expenses/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recurring_expenses"] = RecurringExpense.objects.all()
        return context


class DetailsView(generic.TemplateView):

    template_name = "recurring_expenses/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["expense"] = RecurringExpense.objects.get(pk=kwargs["expense_id"])
        return context


# Create your views here.
class CreateView(View):

    template_name = "recurring_expenses/new.html"

    def get(self, request, *args, **kwargs):
        return render(request, 'recurring_expenses/new.html')

    def post(self, request, *args, **kwargs):
        try:
            recurring_expense = RecurringExpense(
                particulars=request.POST["particulars"],
                currency=request.POST["currency"],
                amount=request.POST["amount"],
                period=request.POST["period"]
            )
            recurring_expense.save()
            # return HttpResponseRedirect(
            #     reverse('recurring_expenses:index', args=(recurring_expense.id,)))
            return HttpResponseRedirect(
                reverse('recurring_expenses:index'))
        except Exception as e:
            print(e)

        return render(request, self.template_name)
