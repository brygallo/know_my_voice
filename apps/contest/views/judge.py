from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from apps.authentication.models import User
from apps.contest.forms import JudgeForm


class BaseFormParticipant:
    model = User
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


class JudgeListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "judge/judge_list.html"


class JudgeDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "judge/judge_detail.html"


class JudgeCreateView(LoginRequiredMixin, BaseFormParticipant, CreateView):
    form_class = JudgeForm
    template_name = "judge/judge_form.html"


class JudgeUpdateView(LoginRequiredMixin, BaseFormParticipant, UpdateView):
    success_message = "Actualizado"
    template_name = "judge/judge_update.html"
    form_class = JudgeForm


class JudgeDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('contest:judge-list')
