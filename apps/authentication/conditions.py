"""File to transitions conditions"""

# Third party integration


def verify_if_user_is_the_boss(instance):
    from tracing.middleware import TracingMiddleware

    information = TracingMiddleware.get_info()
    user = information.get("user", False)
    if user.pk == 1:
        return True
    return False


def verify_if_hitman_is_not_the_boss(instance):
    if instance.pk == 1:
        return False
    return True
