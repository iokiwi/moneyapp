from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.urls import reverse
from django.contrib.auth import get_user_model
import sesame.utils

from .forms import EmailLoginForm


class EmailLoginView(FormView):
    template_name = "users/email_login.html"
    form_class = EmailLoginForm

    def form_valid(self, form):
        # TODO: email magic link to user.
        email = form.cleaned_data["email"]
        User = get_user_model()
        user = User.objects.get(email=email)
        link = get_magic_link(self.request, user)
        form.send_email(link)
        return render(self.request, "users/email_login_success.html")


def get_magic_link(request, user):
    link = reverse("login")
    link = request.build_absolute_uri(link)
    link += sesame.utils.get_query_string(user)
    return link


class UserRegistrationFormView(FormView):
    template_name = "users/register.html"
    form_class = EmailLoginForm

    # TODO: Make this use reverse()
    success_url = "/login/pending/"

    def form_valid(self, form):
        User = get_user_model()
        email = form.cleaned_data["email"]
        user = User(email=email, username=email)
        user.save()
        # TODO: Error handling

        link = get_magic_link(self.request, user)
        form.send_email(link)
        return super().form_valid(form)


class UserRegistrationPendingEmailValidationView(TemplateView):
    template_name = "users/pending_validation.html"
    # form_class = EmailLoginForm
