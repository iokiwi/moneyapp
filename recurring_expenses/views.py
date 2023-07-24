from django.shortcuts import render
from django.views import generic
from .models import RecurringExpense

# from django.http import HttpResponse,
from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render
# from django.contrib import messages
from django.urls import reverse


from .forms import RecurringExpenseForm


def delete_recurring_payment(request, expense_id):
    # if request.method == "GET":
    recurring_expense = RecurringExpense.objects.get(pk=expense_id)
    recurring_expense.delete()
    return HttpResponseRedirect(reverse("recurring_expenses:index"))


def create_or_edit_recurring_payment(request, expense_id=None):
    if expense_id is None:
        create_recurring_payment(request)
    else:
        edit_recurring_payment(request, expense_id=expense_id)


def edit_recurring_payment(request, expense_id):
    recurring_expense = RecurringExpense.objects.get(pk=expense_id)
    if request.method == "POST":
        form = RecurringExpenseForm(request.POST, instance=recurring_expense)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("recurring_expenses:index"))
    elif request.method == "GET":
        form = RecurringExpenseForm(instance=recurring_expense)
        return render(request, "recurring_expenses/edit.html", {"form": form, "expense_id": expense_id})


def create_recurring_payment(request):
    if request.method == "POST":
        form = RecurringExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("recurring_expenses:index"))
    elif request.method == "GET":
        form = RecurringExpenseForm()

    return render(request, "recurring_expenses/new.html", {"form": form})


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
        print(request.POST)
        try:
            recurring_expense = RecurringExpense(
                # active = request.POST["active"],
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
