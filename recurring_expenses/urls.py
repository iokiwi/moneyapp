from django.urls import path
from . import views

app_name = "recurring_expenses"

urlpatterns = [
    # path("stats", views.StatsView.as_view(), name="stats"),
    path("", views.IndexView.as_view(), name="index"),
    path("new/", views.CreateView.as_view(), name="new"),

    # path("import", views.upload, name="import"),
]
