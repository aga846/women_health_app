from django import forms
from django.contrib.auth.models import User
import datetime as dt
from cycles.models import CyclesLength, Temperature


class CyclesLengthForm(forms.ModelForm):

    class Meta():
        model = CyclesLength
        fields = ('length', 'first_day')


class TemperatureForm(forms.ModelForm):

    class Meta():
        model = Temperature
        fields = ('day_of_cycle', 'temperature')
