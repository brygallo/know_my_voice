"""Auth models."""

# Django
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

# Views
from apps.authentication.views import (
    RegisterView,
)

app_name = "auth"

urlpatterns = (
    path(
        route="",
        view=LoginView.as_view(
            template_name="authentication/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path(
        route="register/",
        view=RegisterView.as_view(),
        name="register",
    ),
    path(
        route="logout/",
        view=LogoutView.as_view(),
        name="logout",
    ),

)
