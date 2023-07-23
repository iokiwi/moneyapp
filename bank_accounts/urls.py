from django.urls import path
from . import views

app_name = "bank_accounts"

urlpatterns = [
    # path("stats", views.StatsView.as_view(), name="stats"),
    path("", views.IndexView.as_view(), name="index"),
    # path("import", views.upload, name="import"),
]
