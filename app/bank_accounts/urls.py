from django.urls import path
from . import views

app_name = "bank_accounts"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # path("edit", views.UpdateView.as_view(), name="edit"),
]
