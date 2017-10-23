from django import forms
from django.forms import ModelChoiceField

from . models import Artist, Tilbud, Behov


#The choices html attribute with all artists in th database
class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.navn


class BehovTypeModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj


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


class GodkjennTilbudBookingSjefForm(forms.ModelForm):

    class Meta:
        model = Tilbud
        fields = ('godkjent_av_bookingssjef',)


class GodkjennTilbudManager(forms.ModelForm):

    class Meta:
        model = Tilbud
        fields = ('godkjent_av_manager',)

class LeggTilBehovForm(forms.ModelForm):
    behov_typer = ['instrumenter', 'lyd', 'lys', 'andre']

    #type = BehovTypeModelChoiceField(behov_typer)
    behov = forms.CharField(max_length=200)

    class Meta:
        model = Behov
        fields = ('type', 'behov',)




