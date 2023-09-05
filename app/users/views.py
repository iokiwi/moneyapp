from django.shortcuts import render
from django.views.generic import FormView

from .forms import EmailLoginForm


class EmailLoginView(FormView):
    template_name = "users/email_login.html"
    form_class = EmailLoginForm

    def form_valid(self, form):
        # TODO: email magic link to user.
        return render(self.request, "email_login_success.html")
