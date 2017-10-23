from django import forms
from django.forms import ModelChoiceField

from . models import Artist, Tilbud, Consert


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


class GodkjennTilbudBookingSjefForm(forms.ModelForm):

    class Meta:
        model = Tilbud
        fields = ('godkjent_av_bookingssjef',)


class GodkjennTilbudManager(forms.ModelForm):

    class Meta:
        model = Tilbud
        fields = ('godkjent_av_manager',)

class ArtistForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    sjanger = forms.CharField(max_length=100)
    behov = forms.CharField()

    class Meta:
        model = Artist
        fields = ('navn', 'sjanger', 'behov')


class ConsertForm(forms.ModelForm):
    artist = forms.CharField(max_length=100)
    tidspunkt = forms.DateField()
    sceneNavn = forms.CharField(max_length=250)

    class Meta:
        model = Consert
        fields = ('artist', 'tidspunkt', 'sceneNavn')




