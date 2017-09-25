from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class extend_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=250)

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Extend user'
        verbose_name_plural = 'Extend users'

class rigging(models.Model):
    person = models.ManyToManyField(User)

    def __str__(self):
        return "rigging"

    class Meta:
        verbose_name = 'Rigging'
        verbose_name_plural = 'Rigginger'

class Artist(models.Model):
    navn = models.CharField(max_length=250)
    sjanger = models.CharField(max_length=250)
    krav = models.CharField(max_length=250)

    def __str__(self):
        return self.navn

    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artister'

class Konsert(models.Model):
    artist = models.OneToOneField(Artist)
    tidspunkt = models.DateField()
    sceneNavn = models.CharField(max_length=250, default="Hovedscenen")
    rigging = models.ManyToManyField(rigging)

    def __str__(self):
        return self.artist.navn

    class Meta:
        verbose_name = 'Konsert'
        verbose_name_plural = 'Konserter'


class Tilbud(models.Model):
    a_navn = models.OneToOneField(Konsert)
    pris = models.IntegerField()
    ex_date = models.DateField()

    def __str__(self):
        return "noe smart etter hvert"