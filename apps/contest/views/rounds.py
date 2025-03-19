import random

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from apps.contest.forms import RoundForm, RoundParticipantForm
from apps.contest.mixin import ActiveRoundRequiredMixin
from apps.contest.models import Round, RoundParticipant, RoundParticipantExtraInfo, Participant
from apps.contest.services import RoundContextService
from apps.contest.views.pdf_base import BasePDFView


class BaseFormRound:
    model = Round
    success_message = "Creado"

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Ha ocurrido un error")
        return super().form_invalid(form)

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"Ronda {self.success_message} correctamente",
        )
        return super().form_valid(form)


class RoundListView(LoginRequiredMixin, ListView):
    model = Round

    def get_template_names(self):
        user = self.request.user
        if user.is_judge:
            return ["round/round_list_judge.html"]
        else:
            return ["round/round_list.html"]

    def get_queryset(self):
        user = self.request.user
        if user.is_judge:
            return Round.objects.filter(is_active=True)
        else:
            return Round.objects.all()


class RoundCreateView(LoginRequiredMixin, BaseFormRound, CreateView):
    form_class = RoundForm
    template_name = "round/round_form.html"


class RoundDetailView(LoginRequiredMixin, ActiveRoundRequiredMixin, DetailView):
    model = Round

    def get_template_names(self):
        user = self.request.user
        if user.is_judge:
            return ["round/round_detail_judge.html"]
        else:
            return ["round/round_detail.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        round_instance = self.object
        user = self.request.user

        if user.is_judge:
            rows = RoundContextService.get_judge_context(round_instance, user)
            context['table_rows'] = rows
        else:
            header, rows = RoundContextService.get_non_judge_context(round_instance)
            context['table_header'] = header
            context['table_rows'] = rows

        return context


class RoundUpdateView(LoginRequiredMixin, BaseFormRound, UpdateView):
    success_message = "Actualizado"
    template_name = "round/round_update.html"
    form_class = RoundForm


class RoundDeleteView(LoginRequiredMixin, DeleteView):
    model = Round
    success_url = reverse_lazy('round-list')


# View for Round Participant
class RoundParticipantView(LoginRequiredMixin, UpdateView):
    model = RoundParticipant
    form_class = RoundParticipantForm
    template_name = 'round/round_participant_form.html'

    def dispatch(self, request, *args, **kwargs):
        round_id = self.kwargs.get('round_id')
        self.round = get_object_or_404(Round, pk=round_id)
        self.judge = request.user
        self.participant = get_object_or_404(Participant, pk=self.kwargs.get('participant_id'))

        if not self.round.is_active:
            messages.error(request, "La ronda ya no está activa.")
            return redirect('contest:round-detail', pk=round_id)

        if not self.round.judges.filter(pk=self.judge.pk).exists():
            messages.error(request, "No estás autorizado para calificar en esta ronda.")
            return redirect('contest:round-detail', pk=round_id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['round_id'] = self.kwargs.get('round_id')
        return context

    def get_object(self, queryset=None):
        obj, created = RoundParticipant.objects.get_or_create(
            round=self.round,
            participant=self.participant,
            judge=self.judge,
        )
        return obj

    def get_success_url(self):
        return reverse_lazy('contest:round-detail', kwargs={'pk': self.object.round.pk})

    def form_valid(self, form):
        if not self.round.is_active:
            messages.error(self.request, "La ronda ya no está activa. No se puede registrar la calificación.")
            return redirect('contest:round-detail', pk=self.round.pk)

        response = super().form_valid(form)
        messages.success(self.request, "Calificación registrada correctamente.")
        return response

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, "Ha ocurrido un error")
        return super().form_invalid(form)


class RandomizeParticipantsOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        round_id = kwargs.get('round_id')
        round_instance = get_object_or_404(Round, pk=round_id)
        participants = list(round_instance.participants.all())
        random.shuffle(participants)

        for index, participant in enumerate(participants):
            RoundParticipantExtraInfo.objects.update_or_create(
                round=round_instance, participant=participant,
                defaults={'order': index + 1}
            )
        return redirect('contest:round-detail', pk=round_id)


class MarkAsAbsentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        participant_id = kwargs.get('participant_id')
        round_id = kwargs.get('round_id')
        judge = request.user

        round_instance = get_object_or_404(Round, pk=round_id)
        if not round_instance.is_active:
            messages.error(request, "La ronda ya no está activa. No se puede marcar al participante como ausente.")
            return redirect('contest:round-detail', pk=round_id)

        round_participant = get_object_or_404(RoundParticipant, participant_id=participant_id, round_id=round_id, judge=judge)
        round_participant.presence = 0
        round_participant.vocalization = 0
        round_participant.rhythm = 0
        round_participant.coupling = 0
        round_participant.stage_performance = 0
        round_participant.save()

        messages.success(request, "El participante ha sido marcado como ausente correctamente.")
        return redirect('contest:round-detail', pk=round_id)


class ToggleRoundActiveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        round_id = kwargs.get('round_id')
        round = get_object_or_404(Round, id=round_id)
        round.is_active = not round.is_active
        round.save()
        messages.success(request, f"Estado de la ronda {'activado' if round.is_active else 'desactivado'} correctamente.")
        return redirect('contest:round-detail', pk=round_id)

# PDF REPORTS

class OrderPDFView(BasePDFView):
    template_name = "round/report/order.html"
    open_in_browser = True

    def validate_round(self, round_instance):

        judges_count = round_instance.judges.count()
        participants_count = round_instance.participants.count()
        extra_info_count = RoundParticipantExtraInfo.objects.filter(round=round_instance).count()

        if judges_count == 0 or participants_count == 0:
            return "La ronda debe tener al menos un juez y un participante."

        if extra_info_count < participants_count:
            return "Se debe sortear el orden de participación"

        return None

    def get(self, request, *args, **kwargs):
        round_id = kwargs.get('round_id')
        round_instance = get_object_or_404(Round, id=round_id)
        error_message = self.validate_round(round_instance)

        if error_message:
            messages.error(request, error_message)
            return redirect('contest:round-detail', pk=round_instance.pk)

        context = self.get_context_data(round_id=round_id, round=round_instance)
        self.download_filename = f"lista_participantes_{round_instance.name}.pdf"
        return self.render_to_pdf_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        round_instance = kwargs.get('round')
        if not round_instance:
            round_id = kwargs.get('round_id')
            round_instance = get_object_or_404(Round, id=round_id)
        rows = RoundContextService.get_order_context(round_instance)
        context['table_rows'] = rows
        context['round'] = round_instance
        return context


class ResultsPDFView(BasePDFView):
    template_name = "round/report/results.html"
    open_in_browser = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        round_id = kwargs.get('round_id')
        round_instance = get_object_or_404(Round, id=round_id)
        header, rows = RoundContextService.get_non_judge_context(round_instance)
        context['round'] = round_instance
        context['table_header'] = header
        context['table_rows'] = rows
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        round_instance = context.get('round')

        judges_count = round_instance.judges.count()
        participants_count = round_instance.participants.count()

        if judges_count == 0 or participants_count == 0:
            messages.error(request, "La ronda debe tener al menos un juez y un participante.")
            return redirect('contest:round-detail', pk=round_instance.pk)

        round_participant_count = RoundParticipant.objects.filter(round=round_instance).count()
        expected_califications = judges_count * participants_count

        if round_participant_count < expected_califications:
            messages.error(request, "Para generar el Acta todos los jueces deben calificar a todos los participantes.")
            return redirect('contest:round-detail', pk=round_instance.pk)

        self.download_filename = f"lista_participantes_{round_instance.name}.pdf"
        return self.render_to_pdf_response(context)



class MinutesPDFView(BasePDFView):
    template_name = "round/report/minutes.html"
    open_in_browser = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        round_id = kwargs.get('round_id')
        round_instance = get_object_or_404(Round, id=round_id)

        judges_info = []
        for judge in round_instance.judges.all():
            participants_info = []

            for participant in round_instance.participants.all():
                participant_notes = RoundParticipant.objects.filter(
                    participant=participant,
                    judge=judge,
                    round=round_instance
                ).first()

                if participant_notes:
                    participant_data = {
                        'participant': participant,
                        'presence': participant_notes.presence,
                        'vocalization': participant_notes.vocalization,
                        'rhythm': participant_notes.rhythm,
                        'coupling': participant_notes.coupling,
                        'stage_performance': participant_notes.stage_performance,
                        'total': participant_notes.total_score(),
                    }
                    participants_info.append(participant_data)

            judge_info = {
                'judge': judge,
                'participants': participants_info,
            }
            judges_info.append(judge_info)

        context['judges'] = judges_info
        context['round'] = round_instance

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        round_instance = context.get('round')

        judges_count = round_instance.judges.count()
        participants_count = round_instance.participants.count()

        if judges_count == 0 or participants_count == 0:
            messages.error(request, "La ronda debe tener al menos un juez y un participante.")
            return redirect('contest:round-detail', pk=round_instance.pk)

        round_participant_count = RoundParticipant.objects.filter(round=round_instance).count()
        expected_califications = judges_count * participants_count

        if round_participant_count < expected_califications:
            messages.error(request, "Para generar el Acta, todos los jueces deben calificar a todos los participantes.")
            return redirect('contest:round-detail', pk=round_instance.pk)

        self.download_filename = f"lista_participantes_{round_instance.name}.pdf"
        return self.render_to_pdf_response(context)
