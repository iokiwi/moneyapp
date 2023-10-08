from django.urls import path
from . import views

app_name = "recurring_expenses"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("new/", views.create_recurring_expense, name="new"),
    path("import/", views.import_recurring_expenses, name="import"),
    path("export/", views.export_recurring_expenses, name="export"),
    path("<uuid:expense_id>/edit", views.edit_recurring_expense, name="edit"),
    path("<uuid:expense_id>/delete", views.delete_recurring_expense, name="delete"),
]
