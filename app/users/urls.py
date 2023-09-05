from django.urls import path

from .views import EmailLoginView

urlpatterns = [
    path("", EmailLoginView.as_view(), name="email_login"),
]
