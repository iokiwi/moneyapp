import csv
import requests

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib import messages
from django.urls import reverse

from .models import RecurringExpense
from .forms import RecurringExpenseForm


def get_fxRate_nzd():
    url = "https://api.exchangerate-api.com/v4/latest/NZD"
    response = requests.request("GET", url)
    return response.json()["rates"]


@login_required
def delete_recurring_expense(request, expense_id):
    recurring_expense = RecurringExpense.objects.get(pk=expense_id)
    recurring_expense.delete()
    return HttpResponseRedirect(reverse("recurring_expenses:index"))


@login_required
def create_or_edit_recurring_expense(request, expense_id=None):
    if expense_id is None:
        create_recurring_expense(request)
    else:
        edit_recurring_expense(request, expense_id=expense_id)


def parse_bool(s):
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    raise ValueError("Cannot parse boolean from {}".format(s))


@login_required
def import_recurring_expenses(request):
    if request.method == "GET":
        return render(request, "recurring_expenses/import.html", {})
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")

        if uploaded_file is None:
            messages.error(request, "No file uploaded")
            return HttpResponseRedirect(reverse("recurring_expenses:import"))

        f = uploaded_file.read().decode("utf-8")
        reader = csv.reader(f.splitlines(), delimiter=",")
        next(reader, None)  # skip the headers

        rows_imported = 0
        rows_errored = 0
        total_rows = 0

        for row in reader:
            if row[0].strip(" ").lower() == "totals":
                break

            total_rows += 1

            try:
                recurring_expense = RecurringExpense(
                    active=parse_bool(row[2]),
                    particulars=row[3].strip(" "),
                    amount=row[4].strip("$  "),
                    period=int(row[5]),
                    currency=row[6].strip(" "),
                )
                recurring_expense.save()
                rows_imported += 1
            except Exception as e:
                print(e)
                rows_errored += 1

        messages.success(
            request,
            "{}/{} Recurring expenses imported successfully. {} skipped".format(
                rows_imported, total_rows, rows_errored
            ),
        )

        return HttpResponseRedirect(reverse("recurring_expenses:import"))


@login_required
def edit_recurring_expense(request, expense_id):
    recurring_expense = RecurringExpense.objects.get(pk=expense_id)
    if request.method == "POST":
        form = RecurringExpenseForm(request.POST, instance=recurring_expense)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("recurring_expenses:index"))
    elif request.method == "GET":
        form = RecurringExpenseForm(instance=recurring_expense)
        return render(
            request,
            "recurring_expenses/edit.html",
            {"form": form, "expense_id": expense_id},
        )


@login_required
def create_recurring_expense(request):
    if request.method == "POST":
        form = RecurringExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("recurring_expenses:index"))
    elif request.method == "GET":
        form = RecurringExpenseForm()

    return render(request, "recurring_expenses/new.html", {"form": form})


@login_required
def export_recurring_expenses(request):
    if "csv" in request.GET["format"]:
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="recurring_expenses.csv"'},
        )
        writer = csv.writer(response)
        writer.writerow([
            "Active", "Particulars", "Amount",
            "Currency", "Amount NZD", "Period (Months)",
            ])
        #
        # Get expenses and amount in NZD
        # Copied from class IndexView, maybe this should be a function?
        # Exporting each expense to csv within this though so we don't
        # have to run the for loop twice
        #
        fx_rates = get_fxRate_nzd()
        expenses = RecurringExpense.objects.all()
        for expense in expenses:
            amount_nzd = (1 / fx_rates[expense.currency]) * float(expense.amount)
            expense.amount_nzd = amount_nzd
            writer.writerow([
                expense.active, expense.particulars, format(expense.amount,".2f"), 
                expense.currency, format(expense.amount_nzd,".2f"), expense.period,
                ])
    else:
        response = HttpResponse(status=204)
    
    return response


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "recurring_expenses/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fx_rates = get_fxRate_nzd()
        expenses = RecurringExpense.objects.all()
        for expense in expenses:
            amount_nzd = (1 / fx_rates[expense.currency]) * float(expense.amount)
            expense.amount_nzd = amount_nzd
        context["recurring_expenses"] = expenses
        return context


class DetailsView(LoginRequiredMixin, generic.TemplateView):
    template_name = "recurring_expenses/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["expense"] = RecurringExpense.objects.get(pk=kwargs["expense_id"])
        return context


class CreateView(LoginRequiredMixin, View):
    template_name = "recurring_expenses/new.html"

    def get(self, request, *args, **kwargs):
        return render(request, "recurring_expenses/new.html")

    def post(self, request, *args, **kwargs):
        print(request.POST)
        try:
            recurring_expense = RecurringExpense(
                # active = request.POST["active"],
                particulars=request.POST["particulars"],
                currency=request.POST["currency"],
                amount=request.POST["amount"],
                period=request.POST["period"],
            )
            recurring_expense.save()
            # return HttpResponseRedirect(
            #     reverse('recurring_expensesindex', args=(recurring_expense.id,)))
            return HttpResponseRedirect(reverse("recurring_expenses:index"))
        except Exception as e:
            print(e)

        return render(request, self.template_name)
