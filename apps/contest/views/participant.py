from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.contest.forms import ParticipantForm
from apps.contest.models import Participant


class BaseFormParticipant:
    model = Participant
    success_message = "Creado"

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Ha ocurrido un error")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"Participante  {self.success_message} correctamente ",
        )
        return super().form_valid(form)


class ParticipantListView(LoginRequiredMixin, ListView):
    model = Participant
    template_name = "participants/participant_list.html"


class ParticipantDetailView(LoginRequiredMixin, DetailView):
    model = Participant
    template_name = "participants/participant_detail.html"


class ParticipantCreateView(LoginRequiredMixin, BaseFormParticipant, CreateView):
    form_class = ParticipantForm
    template_name = "participants/participant_form.html"


class ParticipantUpdateView(LoginRequiredMixin, BaseFormParticipant, UpdateView):
    success_message = "Actualizado"
    template_name = "participants/participant_update.html"
    form_class = ParticipantForm


class ParticipantDeleteView(LoginRequiredMixin, DeleteView):
    model = Participant
    success_url = reverse_lazy('contest:participant-list')
