from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.urls import reverse
from django.contrib.auth import get_user_model, logout
from django.views import View
from django.db import IntegrityError
from django.conf import settings

from sesame.utils import get_parameters

from .forms import EmailLoginForm, UserRegistrationForm
import logging

logger = logging.getLogger(__name__)


def get_user(email):
    """Find the user with this email address."""
    User = get_user_model()
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None


def get_magic_link(request, user):
    link = reverse("transactions:index")
    query_params = get_parameters(user)
    link += "?" + urlencode(query_params)
    link = request.build_absolute_uri(link)
    return link


def send_email(user, link):
    """Send an email with this login link to this user."""
    user.email_user(
        subject="[django-sesame] Log in to our app",
        message=f"""\
        Hello,

        You requested that we send you a link to log in to our app:

            {link}

        Thank you for using django-sesame!
        """,
    )


class EmailLoginView(FormView):
    template_name = "users/email_login.html"
    success_url = "/accounts/pending"
    form_class = EmailLoginForm

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user = get_user(email)

        if user is None:
            logger.info("User not found: %s", email)
            return render(self.request, "users/pending_validation.html")

        link = get_magic_link(self.request, user)
        send_email(user, link)

        # If we are in debug mode, show the URL on the screen for convenience
        context = {}
        if settings.DEBUG is True and not settings.ENVIRONMENT.lower().startswith(
            "prod"
        ):
            context["magic_link"] = link

        # NOTE(simonm): We currently do not do a redirect. Resubmitting the form
        # here will result in the post being sent again.
        return render(self.request, "users/pending_validation.html", context=context)


class UserRegistrationFormView(FormView):
    template_name = "users/register.html"
    form_class = UserRegistrationForm
    success_url = "/accounts/pending"

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        try:
            User = get_user_model()
            user = User(email=email, username=email)
            user.set_unusable_password()
            user.save()
        except IntegrityError as e:
            # TODO: Ensure exception gets added to trace
            logger.exception(e)
            # Pretend the form was valid. We don't want to enable enumeration
            # of user accounts.
            return super().form_valid(form)

        link = get_magic_link(self.request, user)
        send_email(user, link)

        context = {}
        if settings.DEBUG is True and not settings.ENVIRONMENT.lower().startswith(
            "prod"
        ):
            context["magic_link"] = link

        super().form_valid(form)

        # NOTE(simonm): We currently do not do a redirect. Resubmitting the form
        # here will result in the post being sent again.
        return render(self.request, "users/pending_validation.html", context=context)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        url = reverse("users:login")
        return redirect(url)


class UserRegistrationPendingEmailValidationView(TemplateView):
    template_name = "users/pending_validation.html"
