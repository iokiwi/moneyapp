from django.shortcuts import render, redirect
from django.views.generic import FormView, TemplateView
from django.urls import reverse
from django.contrib.auth import get_user_model, logout
from urllib.parse import urlencode
from django.views import View

from sesame.utils import get_parameters

from .forms import EmailLoginForm, UserRegistrationForm


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
            # Ignore the case when no user is registered with this address.
            # Possible improvement: send an email telling them to register.
            print("user not found:", email)
            return

        link = get_magic_link(self.request, user)
        send_email(user, link)
        # NOTE(simonm): We currently do not do a redirect. Resubmitting the form
        # here will result in the post being sent again.
        return render(self.request, "users/pending_validation.html")


class UserRegistrationFormView(FormView):
    template_name = "users/register.html"
    form_class = UserRegistrationForm
    success_url = "/accounts/pending"

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        # Create the user if they don't already exist.
        User = get_user_model()
        user = User(email=email, username=email)
        user.set_unusable_password()
        user.save()

        link = get_magic_link(self.request, user)
        send_email(user, link)
        return super().form_valid(form)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        url = reverse("users:login")
        return redirect(url)


class UserRegistrationPendingEmailValidationView(TemplateView):
    template_name = "users/pending_validation.html"
