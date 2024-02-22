from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Participant, Round, Township, RoundParticipant
from ..authentication.models import User


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ["identification", "name", "date_of_birth", "phone_number", "address", "township"]
        widgets = {
            'date_of_birth': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
        }


class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ["name", "date", "judges", "participants", "is_active"]
        widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date'}),
        }


class TownshipForm(forms.ModelForm):
    class Meta:
        model = Township
        fields = '__all__'


class RoundParticipantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RoundParticipantForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['readonly'] = True
            self.fields[field_name].widget.attrs['style'] = 'cursor: pointer;'
            self.fields[field_name].widget.attrs['onfocus'] = 'this.blur();'

    class Meta:
        model = RoundParticipant
        fields = ['coupling', 'intonation', 'expression']


class JudgeForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
