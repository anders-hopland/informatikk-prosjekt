from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy

STATUS_CHOICES = (
    ('arrangor', 'Arrangør'),
    ('lydtekniker', 'Lydtekniker'),
    ('lystekniker', 'Lystekniker'),
    ('manager', 'Manager'),
    ('bookingansvarlig', 'Bookingansvarlig'),
    ('bookingsjef', 'Bookingsjef')
)

SCENER = (
    ('hallen', 'Hallen'),
    ('hovedscenen', 'Hovedscenen'),
    ('storhallen', 'Storhallen')
)

NEED_CHOICES = (
    ('instrumenter', 'Instrumenter'),
    ('lyd', 'Lyd'),
    ('lys', 'Lys'),
    ('andre', 'Andre')
)


'''
INFO
__str__ is for displaying a name in the admin, like a tostring in java
which gives us a better identificator than <model_name>object to work with

verbose_name and verbose_name_plural are defining what each table should
be called in the admin, __str__ defines each isntance

ManyToManyField is lik a many to many relation in SQL, where Django creates the
intermediary table(s)
'''


'''
Extend_user is an extension of the built in User model in Django
We are extending the model because we want to save more data about each user, like
assigning a role to each member
'''
class Extend_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=250, choices=STATUS_CHOICES)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Extend user'
        verbose_name_plural = 'Extend users'

'''
Rigging is just a many to many relation between person and Consert
'''
class Rigging(models.Model):
    person = models.ManyToManyField(User)
    #Tidspunkt for når person skal være med på å rigge
    tidspunkt = models.CharField(max_length=100)

    def __str__(self):
        return "rigging"

    class Meta:
        verbose_name = 'Rigging'
        verbose_name_plural = 'Riggings'


'''
Each user can have many needs, to maintain the integrity of the database,
we must therefore make Behov a new model
'''
class Behov(models.Model):
    type = models.CharField(max_length=250, choices=NEED_CHOICES)
    behov = models.CharField(max_length=250)

    def __str__(self):
        return self.behov


class Artist(models.Model):
    navn = models.CharField(max_length=250)
    sjanger = models.CharField(max_length=250)
    behov = models.ManyToManyField(Behov)

    def __str__(self):
        return self.navn

    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artister'


class Consert(models.Model):
    artist = models.OneToOneField(Artist)
    tidspunkt = models.DateField()
    sceneNavn = models.CharField(max_length=250, choices=SCENER, unique=True)
    rigging = models.ManyToManyField(Rigging)

    def __str__(self):
        return self.artist.navn

    def consert_url(self):
        return reverse('konsert', args=[self.tidspunkt.year, self.tidspunkt.strftime('%m'),
                                        self.tidspunkt.strftime('%d'), self.id])

    class Meta:
        verbose_name = 'consert'
        verbose_name_plural = 'conserts'


#not used yet, will be used in a later sprint
class Tilbud(models.Model):
    a_navn = models.OneToOneField(Consert)
    pris = models.IntegerField()
    ex_date = models.DateField()

    def __str__(self):
        return "noe smart etter hvert"

