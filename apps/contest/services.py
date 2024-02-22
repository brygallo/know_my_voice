# services.py

from .models import Round, RoundParticipant, RoundParticipantExtraInfo


class RoundContextService:
    @staticmethod
    def get_order_context(round_instance):
        rows = []
        for participant in round_instance.participants.all():
            round_participant_info = RoundParticipantExtraInfo.objects.filter(
                round=round_instance, participant=participant
            ).first()

            row = [round_participant_info.order, participant.name]
            rows.append(row)
        rows.sort(key=lambda x: x[0])
        return rows

    @staticmethod
    def get_judge_context(round_instance, user):
        rows = []
        for participant in round_instance.participants.all():
            round_participant = RoundParticipant.objects.filter(
                round=round_instance, participant=participant, judge=user
            ).first()

            round_participant_info = RoundParticipantExtraInfo.objects.filter(
                round=round_instance, participant=participant
            ).first()

            if round_participant_info:
                order = round_participant_info.order
            else:
                order = float('inf')

            if round_participant:
                total_score = round_participant.total_score()
            else:
                total_score = "N/A"

            row = [order, participant.name, total_score, participant.pk]
            rows.append(row)

        rows.sort(key=lambda x: x[0])

        return rows

    @staticmethod
    def get_non_judge_context(round_instance):
        judges = round_instance.judges.all()
        header = ['Identificación'] + ['Participante'] + ["Cantón"] + [judge for judge in judges] + [
            'Total',
            'Acciones']

        rows = []
        for participant in round_instance.participants.all():
            row = [participant.identification, participant.name, participant.township.name]
            total_score = 0
            scores_count = 0

            for judge in judges:
                round_participant = RoundParticipant.objects.filter(round=round_instance, participant=participant,
                                                                    judge=judge).first()
                if round_participant:
                    score = round_participant.total_score() if round_participant else 0
                    if score is not None:
                        total_score += score
                        scores_count += 1
                    row.append(score)
                else:
                    row.append('N/A')

            average_score = round(total_score / scores_count,2) if scores_count > 0 else 0
            row.append(average_score)
            row.append(participant.pk)
            rows.append(row)

        rows.sort(key=lambda x: x[-2], reverse=True)

        return header, rows
