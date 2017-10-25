from django.shortcuts import render, redirect
from django.db.models import Count
from . models import Artist, Consert, Tilbud

from . forms import RegistrerTilbudForm, GodkjennTilbudBookingSjefForm, SendTilbudBookingAnsvarligForm


'''
INFO
A view in Django is a where you pass data to each html page.
A url is connected to a view, and will redirect to the correct view based
on which url it gets passed. The view will in turn query the database for
data, check for user permissions and return the render funcion which in turn
takes three parameters, the request which holds data such as which user is logged
in, an html page and a dictionary with data from the database. The data from the
dictionary will in turn be rendered in the html by the templating engine jinja
'''


def dashboard(request):
    user = request.user
    if not user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'arrangor':
        return redirect('http://127.0.0.1:8000/arrangor/')
    elif rolle == 'lystekniker':
        return redirect('http://127.0.0.1:8000/lystekniker/')
    elif rolle == 'lydtekniker':
        return redirect('http://127.0.0.1:8000/lydtekniker/')
    elif rolle == 'manager':
        return redirect('http://127.0.0.1:8000/manager/')
    elif rolle == 'bookingansvarlig':
        return redirect('http://127.0.0.1:8000/bookingansvarlig/')
    elif rolle == 'bookingsjef':
        return redirect('http://127.0.0.1:8000/bookingsjef/')
    else:
        return render(request, 'registration/login.html', {})


def arrangor(request):
    user = request.user

    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'arrangor':
        current_consert = request.POST.get('scene-choices')
        if current_consert is not None and current_consert != 'alle':
            object_list = Consert.objects.filter(sceneNavn=current_consert).order_by('tidspunkt')
        else:
            object_list = Consert.objects.all().order_by('tidspunkt')

        scene_list = Consert.objects.values('sceneNavn').distinct()

        return render(request, 'app/arrangor.html', {'conserts': object_list,
                                                     'rolle': rolle,
                                                     'sceneliste': scene_list,
                                                     'current_consert': current_consert})
    else:
        return render(request, 'dashboard', {'rolle': rolle})

def lydtekniker(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'lydtekniker':
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/lydtekniker.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'dashboard', {'rolle': rolle})

def lystekniker(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'lystekniker':
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/lystekniker.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'dashboard', {'rolle': rolle})

def konsert(request, year, month, day, post_id):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'arrangor' or rolle == 'bookingansvarlig' or rolle == 'manager':
        object_list = Consert.objects.filter(id=post_id)

        lysteknikere = {}
        lydteknikere = {}
        andre = {}

        for consert in Consert.objects.filter(id=post_id).all():
            for rigging in consert.rigging.all():
                for person in rigging.person.all():
                    if person.profile.role == 'lystekniker':
                        lysteknikere[person] = person
                    elif person.profile.role == 'lydtekniker':
                        lydteknikere[person] = person
                    else:
                        andre[person] = person

        instrument_list = {}
        annet_list = {}
        lyd_list = {}
        lys_list = {}

        for consert in Consert.objects.filter(id=post_id).all():
            for behov in consert.artist.behov.all():
                if behov.type == 'instrumenter':
                    instrument_list[behov] = behov
                elif behov.type == 'andre':
                    annet_list[behov] = behov
                elif behov.type == 'lyd':
                    lyd_list[behov] = behov
                elif behov.type == 'lys':
                    lys_list[behov] = behov

        return render(request, 'app/konsert.html', {'conserts': object_list,
                                                    'rolle': rolle,
                                                    'instruments': instrument_list,
                                                    'annet_list': annet_list,
                                                    'lyd_list': lyd_list,
                                                    'lys_list': lys_list,
                                                    'lysteknikere': lysteknikere,
                                                    'lydteknikere': lydteknikere,
                                                    'andre': andre,
                                                    })
    else:
        return render(request, 'dashboard', {'rolle': rolle})


def detaljer_scener(request, navn):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'arrangor':
        object_list = Consert.objects.filter(sceneNavn=navn)
        return render(request, 'app/sceneDetaljer.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'dashboard', {'rolle': rolle})


def bookingansvarlig(request):
    user = request.user
    if not user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig':
        current_consert = request.POST.get('scene-choices')
        if current_consert is not None and current_consert != 'alle':
            object_list = Consert.objects.order_by('tidspunkt')
        else:
            object_list = Consert.objects.all().order_by('tidspunkt')

        scene_list = Consert.objects.values('sceneNavn').distinct()

        return render(request, 'app/bookingansvarlig.html', {'conserts': object_list,  'rolle': rolle, 'sceneliste': scene_list, 'current_consert': current_consert})
    else:
        return render(request, 'dahsboard', {'rolle': rolle})

def tidligere_konserter(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig':
        current_genre = request.POST.get('sjanger-choices')
        if current_genre is not None and current_genre != 'alle':
            concert_list = Consert.objects.filter(artist__sjanger=current_genre).exclude(tidspunkt__year='2017')
        else:
            concert_list = Consert.objects.exclude(tidspunkt__year='2017')

        sjanger_list = Artist.objects.values('sjanger').distinct()

        return render(request, 'app/tidligere_konserter.html', {'conserts': concert_list, 'rolle': rolle, 'sjangerliste': sjanger_list, 'current_genre': current_genre})
    else:
        return render(request, 'app/dashboard.html', {'rolle': rolle})

def bookingsjef(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingsjef':
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/manager.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'dashboard', {'rolle': rolle})


def manager(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'manager':

        current_artist = request.POST.get('artist-choices')

        if current_artist is not None and current_artist != 'velgBand':
            object_list = Artist.objects.filter(manager=user.profile).order_by('navn')
        else:
            object_list = Artist.objects.all().order_by('navn')

        return render(request, 'app/manager.html', {'artists': object_list,
                                                    'rolle': rolle,
                                                    'current_artist': current_artist
                                                    })
    else:
        return redirect('dashboard')


def redigerband(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'manager':
        object_list = Artist.objects.filter(manager=user.profile).order_by('navn')
        return render(request, 'app/redigerBand.html', {'artists': object_list, 'rolle': rolle})
    else:
        return render(request, 'dashboard', {'rolle': rolle})


def artist(request, navn):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'manager':
        band = Artist.objects.get(slug=navn)
        object_list = Consert.objects.filter(artist=band)
        return render(request, 'app/artist.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'dashboard', {'rolle': rolle})


def band_search(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    return render(request, 'dashboard', {'rolle': rolle})


def lag_tilbud(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig':
        if request.method == 'POST':
            form = RegistrerTilbudForm(request.POST)
            if form.is_valid():
                form.save()
                redirect('dashboard')
        form = RegistrerTilbudForm()
        return render(request, 'app/lag_tilbud.html', {'form': form, 'rolle': rolle})
    else:
        return render(request, 'dashboard', {'rolle': rolle})


#Bookingsjef får liste over tilbud og kan godkjenne
def tilbud_liste_bookingsjef(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingsjef':
        object_list = Tilbud.objects.filter(godkjent_av_bookingssjef=None)
        #num_conserts = Consert.objects.filter(tidspunkt__year=2017).count()

        return render(request, 'app/tilbud_liste_bookingsjef.html', {'tilbuds': object_list, 'rolle': rolle})
    else:
        return render(request, 'dashboard', {'rolle': rolle})


def godkjenn_tilbud_bookingsjef(request, tilbud_id):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingsjef':
        tilbud = Tilbud.objects.get(id=tilbud_id)
        form = GodkjennTilbudBookingSjefForm(instance=tilbud)

        if request.method == 'POST':
            form = GodkjennTilbudBookingSjefForm(request.POST, instance=tilbud)
            if form.is_valid():
                form.save()
                return redirect('tilbud_liste_bookingsjef')

        return render(request, 'app/godkjenn_tilbud_bookingsjef.html', {'tilbud': tilbud, 'form': form, 'rolle': rolle})
    else:
        return render(request, 'dashboard', {'rolle': rolle})


#Bookingansvarlig får godkjent tilbud og sender videre
def tilbud_liste_bookingansvarlig(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig':
        object_list = Tilbud.objects.filter(godkjent_av_bookingssjef=True, sendt_av_ansvarlig=None)
        #num_conserts = Consert.objects.filter(tidspunkt__year=2017).count()

        return render(request, 'app/tilbud_liste_bookingansvarlig.html', {'tilbuds': object_list, 'rolle': rolle})
    else:
        return render(request, 'dashboard', {'rolle': rolle})



def send_tilbud_bookingansvarlig(request, tilbud_id):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig':
        tilbud = Tilbud.objects.get(id=tilbud_id)
        form = SendTilbudBookingAnsvarligForm(instance=tilbud)

        if request.method == 'POST':
            form = SendTilbudBookingAnsvarligForm(request.POST, instance=tilbud)
            if form.is_valid():
                form.save()
                return redirect('tilbud_liste_bookingansvarlig')

        return render(request, 'app/send_tilbud_bookingansvarlig.html', {'tilbud': tilbud, 'form': form, 'rolle': rolle})
    else:
        return render(request, 'dashboard', {'rolle': rolle})

