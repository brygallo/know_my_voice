"""Transitions views file"""
# Django
from django.views.generic import View
from django.http import JsonResponse
from django.apps import apps


class TransitionView(View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        transition = kwargs.get("transition")
        instance = self.get_object()
        if not hasattr(instance, transition):
            return JsonResponse(
                {"error": "%s does not exists." % transition}, status=400
            )
        method = getattr(instance, transition)
        method(**self.get_kwargs())
        instance.save()
        return JsonResponse(
            {"message": "%s executed successfully" % transition}, status=200
        )

    def get_kwargs(self):
        kwargs = {"user": self.request.user}
        return kwargs

    def get_object(self):
        app_name = self.kwargs.get("app")
        model_name = self.kwargs.get("model")
        pk = self.kwargs.get("pk")
        model_class = apps.get_model(app_name, model_name)
        if hasattr(model_class, "slug"):
            instance = model_class.objects.get(slug=pk)
        else:
            instance = model_class.objects.get(pk=pk)

        return instance
