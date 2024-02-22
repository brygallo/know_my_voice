from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse


class Participant(models.Model):
    identification = models.CharField(max_length=16, primary_key=True, verbose_name="Cedula")
    name = models.CharField(max_length=128, verbose_name="Nombres completos")
    date_of_birth = models.DateField(verbose_name="Fecha de Nacimiento")
    phone_number = models.CharField(max_length=15, blank=True, verbose_name="Numero de Télefono")
    address = models.TextField(blank=True, verbose_name="Dirección")
    township = models.ForeignKey('Township', on_delete=models.PROTECT, null=True, blank=False, verbose_name="Cantón")

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def get_detail_url(self):
        return reverse(
            "contest:participant-detail",
            args=[
                self.pk,
            ],
        )

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_list_url(self):
        return reverse("contest:participant-list")

    def __str__(self):
        return self.name


class Round(models.Model):
    name = models.CharField(max_length=128, verbose_name="Nombre")
    date = models.DateField(verbose_name="Fecha")
    judges = models.ManyToManyField(
        "authentication.User",
        related_name="judges_rounds",
        verbose_name="Jueces"
    )
    participants = models.ManyToManyField(Participant, related_name='round', verbose_name="Participantes")
    is_active = models.BooleanField(default=False, verbose_name="Está Activa")

    def save(self, *args, **kwargs):
        if self.is_active:
            Round.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def get_detail_url(self):
        return reverse(
            "contest:round-detail",
            args=[
                self.pk,
            ],
        )

    def get_absolute_url(self):
        return self.get_detail_url()

    def get_list_url(self):
        return reverse("contest:round-list")

    def __str__(self):
        return self.name


class RoundParticipant(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="participants_details")
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT, null=True, blank=False)
    judge = models.ForeignKey("authentication.User", on_delete=models.PROTECT, verbose_name="Juez", null=True,
                              blank=False)

    coupling = models.PositiveSmallIntegerField(
        verbose_name="Acoplamiento en el Ritmo (35 pts)",
        null=True, blank=False, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(35)])
    intonation = models.PositiveSmallIntegerField(
        verbose_name="Entonación Afinación (35 pts)",
        null=True, blank=False, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(35)])
    expression = models.PositiveSmallIntegerField(
        verbose_name="Expresion e interpretación (30 pts)",
        null=True, blank=False, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(30)])

    def __str__(self):
        return f"{self.round.name} - {self.participant.name}"

    def total_score(self):
        total = 0
        if self.coupling:
            total += self.coupling
        if self.intonation:
            total += self.intonation
        if self.expression:
            total += self.expression
        return total


class RoundParticipantExtraInfo(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="extra_info")
    participant = models.ForeignKey(Participant, on_delete=models.PROTECT, null=True, blank=False)
    likes = models.IntegerField(verbose_name="Likes", null=True, blank=False)
    order = models.IntegerField(verbose_name="Orden", null=True, blank=False)
    rated = models.BooleanField(verbose_name="Calificado", default=False)


class Township(models.Model):
    name = models.CharField(max_length=128, verbose_name="Nombre")

    def __str__(self):
        return self.name
