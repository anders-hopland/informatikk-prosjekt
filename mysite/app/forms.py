from django import forms
from django.forms import ModelChoiceField

from . models import Artist, Tilbud, Behov


#The choices html attribute with all artists in th database
class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.navn


#The choices html attribute with all artists in th database
class BehovTypeModelChoiceField(ModelChoiceField):
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


class SendTilbudBookingAnsvarligForm(forms.ModelForm):

    class Meta:
        model = Tilbud
        fields = ('sendt_av_ansvarlig',)


class LeggTilBehovForm(forms.ModelForm):
    type = BehovTypeModelChoiceField()
    behov = forms.CharField(max_length=200)

    class Meta:
        model = Behov
        fields = ('type', 'behov',)

