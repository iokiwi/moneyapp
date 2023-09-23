from django.urls import path

from .views import (
    EmailLoginView,
    UserRegistrationFormView,
    UserRegistrationPendingEmailValidationView
)
from sesame.views import LoginView

urlpatterns = [
    path("", EmailLoginView.as_view(), name="email_login"),
    path("auth/", LoginView.as_view(), name="login"),
    path("register/", UserRegistrationFormView.as_view(), name="register"),
    path("pending/", UserRegistrationPendingEmailValidationView.as_view(), name="pending")
]
