from django import forms
from . models import Tilbud

class LageTilbudForm(forms.ModelForm):

    class Meta:
        model = Tilbud
        fields = ('artist', 'prist', 'date')



