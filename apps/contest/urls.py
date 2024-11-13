from django.urls import path

from apps.contest.views.judge import JudgeListView, JudgeCreateView, JudgeUpdateView, JudgeDeleteView, JudgeDetailView
from apps.contest.views.participant import ParticipantListView, ParticipantCreateView, ParticipantDetailView, \
    ParticipantUpdateView, ParticipantDeleteView
from apps.contest.views.rounds import RoundListView, RoundCreateView, RoundDetailView, RoundUpdateView, RoundDeleteView, \
    RoundParticipantView, RandomizeParticipantsOrderView, ResultsPDFView, MinutesPDFView, OrderPDFView, \
    MarkAsAbsentView, ToggleRoundActiveView
from apps.contest.views.township import TownshipListView, TownshipCreateView, TownshipUpdateView, TownshipDeleteView

app_name = "contest"
urlpatterns = (
    # URLs para Participant
    path('participants/', ParticipantListView.as_view(), name="participant-list", ),
    path('participant/create/', ParticipantCreateView.as_view(), name="participant-create", ),
    path('participant/<pk>/', ParticipantDetailView.as_view(), name="participant-detail", ),
    path('participant/<pk>/update/', ParticipantUpdateView.as_view(), name='participant-update', ),
    path('participant/<pk>/delete/', ParticipantDeleteView.as_view(), name='participant-delete'),

    # URLs para Round
    path('rounds/', RoundListView.as_view(), name='round-list'),
    path('round/create/', RoundCreateView.as_view(), name='round-create'),
    path('round/<pk>/', RoundDetailView.as_view(), name='round-detail'),
    path('round/<pk>/update/', RoundUpdateView.as_view(), name='round-update'),
    path('round/<pk>/delete/', RoundDeleteView.as_view(), name='round-delete'),

    path('round/<int:round_id>/participant/<str:participant_id>/rate/', RoundParticipantView.as_view(),
         name='round-participant'),

    path('round/<int:round_id>/randomize/', RandomizeParticipantsOrderView.as_view(),
         name='randomize_participants_order'),

    path('results/pdf/<int:round_id>/', ResultsPDFView.as_view(), name='results_pdf'),

    path('minutes/pdf/<int:round_id>/', MinutesPDFView.as_view(), name='minutes_pdf'),
    path('order/pdf/<int:round_id>/', OrderPDFView.as_view(), name='order_pdf'),

    path('round/<int:round_id>/participant/<str:participant_id>/mark_absent/', MarkAsAbsentView.as_view(), name='round-mark-absent'),
    path('round/<int:round_id>/toggle_active/', ToggleRoundActiveView.as_view(), name='toggle-round-active'),

    # URLs para Township
    path('townships/', TownshipListView.as_view(), name='township-list'),
    path('township/create/', TownshipCreateView.as_view(), name='township-create'),
    path('township/<pk>/update/', TownshipUpdateView.as_view(), name='township-update'),
    path('township/<pk>/delete/', TownshipDeleteView.as_view(), name='township-delete'),

    # URLs para Judge
    path('judge/', JudgeListView.as_view(), name='judge-list'),
    path('judge/create/', JudgeCreateView.as_view(), name='judge-create'),
    path('judge/<pk>/', JudgeDetailView.as_view(), name="judge-detail", ),
    path('judge/<pk>/update/', JudgeUpdateView.as_view(), name='judge-update'),
    path('judge/<pk>/delete/', JudgeDeleteView.as_view(), name='judge-delete'),
)
