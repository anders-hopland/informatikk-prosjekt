from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class extend_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=250)

class rigging(models.Model):
    person = models.ManyToManyField(extend_user)

class Artist(models.Model):
    navn = models.CharField(max_length=250)
    sjanger = models.CharField(max_length=250)
    krav = models.CharField(max_length=250)

class Konsert(models.Model):
    a_navn = models.OneToOneField(Artist)
    s_tidspunkt = models.DateField()
    rigging = models.ManyToManyField(rigging)


class Tilbud(models.Model):
    a_navn = models.OneToOneField(Konsert)
    pris = models.IntegerField()
    ex_date = models.DateField()