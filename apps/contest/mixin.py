from django.contrib import messages
from django.shortcuts import redirect


class ActiveRoundRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        round_instance = self.get_object()

        if request.user.is_judge and not round_instance.is_active:
            messages.error(request, "La ronda ya no está activa.")
            return redirect('contest:round-list')

        return super().dispatch(request, *args, **kwargs)
