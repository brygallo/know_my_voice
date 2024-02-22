from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.contest.forms import TownshipForm
from apps.contest.models import Township


class BaseFormTownship:
    model = Township
    success_message = "Creado"

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Ha ocurrido un error")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"Cantón  {self.success_message} correctamente ",
        )
        return super().form_valid(form)


class TownshipListView(LoginRequiredMixin, ListView):
    model = Township
    template_name = "township/township_list.html"


class TownshipCreateView(LoginRequiredMixin, BaseFormTownship, CreateView):
    form_class = TownshipForm
    template_name = "township/township_form.html"
    success_url = reverse_lazy('contest:township-list')


class TownshipUpdateView(LoginRequiredMixin, BaseFormTownship, UpdateView):
    success_message = "Actualizado"
    template_name = "township/township_update.html"
    form_class = TownshipForm
    success_url = reverse_lazy('contest:township-list')


class TownshipDeleteView(LoginRequiredMixin, DeleteView):
    model = Township
    success_url = reverse_lazy('contest:township-list')
