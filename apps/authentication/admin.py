""" Audit model admin """

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


# Models
from apps.authentication.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    pass


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    pass
