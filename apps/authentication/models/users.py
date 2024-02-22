"""User model."""

# Django
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse

# Third party integration
from django_fsm import FSMIntegerField, transition

# Conditions
from apps.authentication.conditions import (
    verify_if_user_is_the_boss,
    verify_if_hitman_is_not_the_boss,
)


class User(AbstractUser):
    """User model.

    Extend from Django's Abstract User, change the username field
    to email and add some extra fields.
    """

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    description = models.TextField(default="")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]
    is_judge = models.BooleanField(default=True, verbose_name="Es Juez")

    class Meta:
        ordering = ("pk",)

    def __str__(self):
        """Return username."""
        return f"{self.get_full_name()}"

    def get_detail_url(self):
        return reverse(
            "contest:judge-detail",
            args=[
                self.pk,
            ],
        )

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_list_url(self):
        return reverse("contest:judge-list")
