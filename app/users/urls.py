from django.urls import path

from .views import (
    EmailLoginView,
    UserRegistrationFormView,
    UserRegistrationPendingEmailValidationView,
)

from sesame.views import LoginView

app_name = "users"
urlpatterns = [
    path("", EmailLoginView.as_view(), name="login"),
    path("auth/", LoginView.as_view(), name="auth"),
    path("signup/", UserRegistrationFormView.as_view(), name="sign_up"),
    path(
        "pending/", UserRegistrationPendingEmailValidationView.as_view(), name="pending"
    ),
]
