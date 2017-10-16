from django import forms
from django.forms import ModelChoiceField

from . models import Artist, Tilbud


#The choices html attribute with all artists in th database
class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.navn


class RegistrerTilbudForm(forms.ModelForm):
    artist = MyModelChoiceField(queryset=Artist.objects.all())
    soknad = forms.CharField(widget=forms.Textarea)
    pris = forms.CharField()

    class Meta:
        model = Tilbud
        fields = [
            'artist',
            'soknad',
            'pris',
            ]

    def save(self):
        tilbud = super(RegistrerTilbudForm, self).save(commit=False)
        tilbud.save()
        return tilbud
'''
class GodkjennTilbudBookingAnsvarligForm(forms.ModelForm):
    class Meta:
        model = Tilbud

    def __init__(self, *args, **kwargs):
        current_tilbud = kwargs.pop('current_tilbud')
        self.fields['godkjent'] = forms.BooleanField(
            label='myLabel',
            required=False,
            initial=False
        )

    def save(self):
        tilbud = super(RegistrerTilbudForm, self).save(commit=False)
        tilbud.save()
        return tilbud

'''


