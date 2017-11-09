from django import forms
from django.forms import ModelChoiceField

from . models import Artist, Tilbud, Behov, Consert

MESSAGE_STATUS = (
    (True, "Ja"),
    (False, "Nei")
)

SCENER = (
    ('hallen', 'Hallen'),
    ('hovedscenen', 'Hovedscenen'),
    ('storhallen', 'Storhallen')
)


class BehovTypeModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj


class RegistrerTilbudForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegistrerTilbudForm, self).__init__(*args, **kwargs)

        #Have to load choices each time
        artist_choices = tuple(Artist.objects.all().values_list('id', 'navn'))
        self.fields['artist'].choices = artist_choices


    class Meta:
        model = Tilbud
        fields = [
            'artist',
            'soknad',
            'pris',
            'tidspunkt',
            'scene_navn'
            ]

    def save(self):
        tilbud = super(RegistrerTilbudForm, self).save()
        return tilbud

    artist = forms.Select(choices=Artist.objects.all())
    soknad = forms.CharField(widget=forms.Textarea)
    pris = forms.IntegerField()
    tidspunkt = forms.DateField(widget=forms.SelectDateWidget())
    scene_navn = forms.Select(choices=SCENER)


class SendTilbudBookingAnsvarligForm(forms.ModelForm):

    class Meta:
        model = Tilbud
        fields = ('sendt_av_ansvarlig',)
        labels = {
            'sendt_av_ansvarlig': 'Godkjenn og send'
        }
        widgets = {
            'sendt_av_ansvarlig': forms.RadioSelect(choices=MESSAGE_STATUS),

        }


class GodkjennTilbudManagerForm(forms.ModelForm):

    class Meta:
        model = Tilbud
        fields = ('godkjent_av_manager',)
        labels = {
            'godkjent_av_manager': 'Godkjenn og book konsert'
        }
        widgets = {
            'godkjent_av_manager': forms.RadioSelect(choices=MESSAGE_STATUS),

        }


class GodkjennTilbudBookingSjefForm(forms.ModelForm):

    class Meta:
        model = Tilbud
        fields = ('godkjent_av_bookingsjef',)
        labels = {
            'godkjent_av_bookingsjef': 'Godkjenn og send'
        }
        widgets = {
            'godkjent_av_bookingsjef': forms.RadioSelect(choices=MESSAGE_STATUS),

        }

class LeggTilBehovForm(forms.ModelForm):

    class Meta:
        model = Behov
        fields = ('type', 'behov',)

