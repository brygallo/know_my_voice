"""Auth models."""

# Django

from django.urls import path

# Local
from apps.transitions.views import TransitionView

app_name = "transitions"

urlpatterns = (
    path(
        route="transition/<slug:transition>/<slug:app>/<slug:model>/<int:pk>/",
        view=TransitionView.as_view(),
        name="transition",
    ),
)
