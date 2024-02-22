# Django
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import  CreateView


# Forms
from apps.authentication.forms import RegisterForm

User = get_user_model()


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "authentication/register.html"
    success_url = reverse_lazy("auth:login")

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, "Successfully hitman registered"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "An error has occurred")
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)





