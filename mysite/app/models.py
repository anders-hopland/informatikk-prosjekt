from django.db import models

# Create your models here.
from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('arrangor', 'Arrangør'),
    ('lydtekniker', 'Tekniker'),
    ('lystekniker', 'Lystekniker'),
    ('manager', 'Manager'),
    ('bookingansvarlig', 'Bookingansvarlig'),
    ('bookingsjef', 'Bookingsjef')
)

class Extend_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=250, choices=STATUS_CHOICES)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Extend user'
        verbose_name_plural = 'Extend users'

class Rigging(models.Model):
    person = models.ManyToManyField(User)

    def __str__(self):
        return "rigging"

    class Meta:
        verbose_name = 'Rigging'
        verbose_name_plural = 'Riggings'

class Artist(models.Model):
    navn = models.CharField(max_length=250)
    sjanger = models.CharField(max_length=250)
    krav = models.CharField(max_length=250)

    def __str__(self):
        return self.navn

    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artister'

class Consert(models.Model):
    artist = models.OneToOneField(Artist)
    tidspunkt = models.DateField()
    sceneNavn = models.CharField(max_length=250, default="Hovedscenen")
    rigging = models.ManyToManyField(Rigging)

    def __str__(self):
        return self.artist.navn

    class Meta:
        verbose_name = 'consert'
        verbose_name_plural = 'conserts'


class Tilbud(models.Model):
    a_navn = models.OneToOneField(Consert)
    pris = models.IntegerField()
    ex_date = models.DateField()

    def __str__(self):
        return "noe smart etter hvert"