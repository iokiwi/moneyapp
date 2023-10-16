import csv
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib import messages
from django.urls import reverse

from moneyapp.helpers import parse_bool

from datetime import datetime

from .models import RecurringExpense
from .forms import RecurringExpenseForm

EXPORT_FORMATS = [
    "csv",
    "json",
]


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


def get_filename(format):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return "recurring_expenses_{}.{}".format(timestamp, format.lower())


def export_to_csv(expenses):
    filename = get_filename("csv")
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
    writer = csv.writer(response)
    writer.writerow(
        [
            "id",
            "active",
            "particulars",
            "amount",
            "currency",
            "amount_nzd",
            "period",
        ]
    )

    for expense in expenses:
        writer.writerow(
            [
                expense.id,
                expense.active,
                expense.particulars,
                format(expense.amount, ".2f"),
                expense.currency,
                format(expense.amount_nzd, ".2f"),
                expense.period,
            ]
        )
        return response


def export_to_json(expenses):
    data = []
    filename = get_filename("json")
    for expense in expenses:
        data.append(
            {
                "id": str(expense.id),
                "active": expense.active,
                "particulars": expense.particulars,
                "amount": format(expense.amount, ".2f"),
                "currency": expense.currency,
                "amount_nzd": format(expense.amount_nzd, ".2f"),
                "period": expense.period,
            }
        )

    json_data = json.dumps(data)

    response = HttpResponse(
        content_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
    response.write(json_data)
    return response


@login_required
def export_recurring_expenses(request, export_format):
    # Assuring that the url parameter is not case-sensitive.
    export_format = export_format.lower()

    if export_format not in EXPORT_FORMATS:
        messages.error(request, f"{export_format} is not a valid format")
        return redirect("recurring_expenses:index")

    expenses = RecurringExpense.objects.all()
    if export_format == "csv":
        return export_to_csv(expenses)
    elif export_format == "json":
        return export_to_json(expenses)


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "recurring_expenses/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expenses = RecurringExpense.objects.all()

        for expense in expenses:
            print(expense.amount_nzd)

        context["recurring_expenses"] = expenses
        context["export_formats"] = EXPORT_FORMATS
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
