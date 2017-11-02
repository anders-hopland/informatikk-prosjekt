from django import forms
from django.forms import ModelChoiceField

from . models import Artist, Tilbud, Behov

MESSAGE_STATUS = (
    (True, "Yes I acknowledge this"),
    (False, "No, I do not like this")
)

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
    pris = forms.IntegerField()
    tidspunkt = forms.DateField(widget=forms.SelectDateWidget())

    class Meta:
        model = Tilbud
        fields = [
            'artist',
            'soknad',
            'pris',
            'tidspunkt'
            ]

    def save(self):
        tilbud = super(RegistrerTilbudForm, self).save(commit=False)
        tilbud.save()
        return tilbud


class GodkjennTilbudBookingSjefForm(forms.ModelForm):

    class Meta:
        model = Tilbud
        fields = ('godkjent_av_bookingssjef',)
        widgets = {
            'sendt_av_ansvarlig': forms.RadioSelect(choices=MESSAGE_STATUS),
        }


class SendTilbudBookingAnsvarligForm(forms.ModelForm):

    class Meta:
        model = Tilbud
        fields = ('sendt_av_ansvarlig',)
        widgets = {
            'sendt_av_ansvarlig': forms.RadioSelect(choices=MESSAGE_STATUS),
        }


class GodkjennTilbudManagerForm(forms.ModelForm):

    class Meta:
        model = Tilbud
        fields = ('godkjent_av_bookingssjef',)
        widgets = {
            'sendt_av_ansvarlig': forms.RadioSelect(choices=MESSAGE_STATUS),
        }


class LeggTilBehovForm(forms.ModelForm):

    class Meta:
        model = Behov
        fields = ('type', 'behov',)

