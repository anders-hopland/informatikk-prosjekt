from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

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

STATUS_FOR_TILBUD = (
    (None, "Ubehandlet"),
    (True, "Godkjenn"),
    (False, "Avslå")
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
    tidspunkt_for_konsert = models.CharField(max_length=100)
    tidspunkt_etter_konsert = models.CharField(max_length=100)

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
    navn = models.CharField(max_length=250, unique=True)
    sjanger = models.CharField(max_length=250)
    manager = models.ManyToManyField(Extend_user)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return self.navn

    def create_slug(self):
        self.slug = self.navn.replace(' ','_')

    def save(self, *args, **kwargs):
        self.create_slug()
        super().save()

    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artister'


class Consert(models.Model):
    artist = models.ForeignKey(Artist, related_name='concert')
    behov = models.ManyToManyField(Behov, blank=True)
    tidspunkt = models.DateField()
    sceneNavn = models.CharField(max_length=250, choices=SCENER)
    rigging = models.ManyToManyField(Rigging, blank=True)
    tilskuertall = models.IntegerField(default=0, blank=True)
    inntekter = models.IntegerField(default=0, blank=True)
    nokkelInfo = models.TextField(blank=True)
    kostnader = models.IntegerField(default=0, blank=True)
    billettpris = models.IntegerField(editable=False, null=True)

    def __str__(self):
        return self.artist.navn

    def consert_url(self):
        return reverse('konsert', args=[self.tidspunkt.year, self.tidspunkt.strftime('%m'),
                                        self.tidspunkt.strftime('%d'), self.id])

    def band_detaljer_url(self):
        return reverse('band_detaljer', args=[self.id])

    class Meta:
        verbose_name = 'consert'
        verbose_name_plural = 'conserts'
        unique_together = ('tidspunkt', 'sceneNavn')


#not used yet, will be used in a later sprint
class Tilbud(models.Model):
    artist = models.ForeignKey(Artist)
    soknad = models.TextField()
    pris = models.IntegerField()
    tidspunkt = models.DateField()
    scene_navn = models.CharField(max_length=250, choices=SCENER)
    godkjent_av_bookingsjef = models.NullBooleanField(blank=True, null=True, default=None)
    sendt_av_ansvarlig = models.NullBooleanField(blank=True, null=True, default=None)
    godkjent_av_manager = models.NullBooleanField(blank=True, null=True, default=None)

    def __str__(self):
        return 'tilbud til ' + str(self.artist.navn)

    class Meta:
        verbose_name = 'tilbud'
        verbose_name_plural = 'tilbud'

class Band_Info(models.Model):
    band = models.CharField(max_length=250)
    nokkelInfo = models.TextField()
    stromtjeneste = models.TextField()
    albumSalg = models.TextField()
    norskeKonserter = models.TextField()

    def __str__(self):
        return self.band

    class Meta:
        verbose_name = 'Band Info'
        verbose_name_plural = 'Band Information'