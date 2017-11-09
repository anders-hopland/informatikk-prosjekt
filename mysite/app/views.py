from django.shortcuts import render, redirect
from django.contrib import messages

from . models import Artist, Consert, Tilbud, Behov, Band_Info
from datetime import datetime, timedelta
import math

from . forms import LeggTilBehovForm, SendTilbudBookingAnsvarligForm, GodkjennTilbudManagerForm
from . forms import RegistrerTilbudForm, GodkjennTilbudBookingSjefForm

from django.db.models import Q

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

SCENER = ['hallen', 'hovedscenen', 'storhallen']


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
            object_list = Consert.objects.filter(
                sceneNavn=current_consert).order_by(
                'tidspunkt').exclude(
                ~Q(tidspunkt__year='2018'))
        else:
            object_list = Consert.objects.all().order_by(
                'tidspunkt').exclude(
                ~Q(tidspunkt__year='2018'))

        scene_list = Consert.objects.values('sceneNavn').distinct()

        return render(request, 'app/arrangor.html', {'conserts': object_list,
                                                     'rolle': rolle,
                                                     'sceneliste': scene_list,
                                                     'current_consert': current_consert})
    else:
        return redirect('dashboard')

def lydtekniker(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'lydtekniker':
        object_list = Consert.objects.filter(
            rigging__person__username=user.username).order_by(
            'tidspunkt').exclude(
            ~Q(tidspunkt__year='2018'))
        return render(request, 'app/lydtekniker.html', {'conserts': object_list,
                                                        'rolle': rolle})
    else:
        return redirect('dashboard')

def lystekniker(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'lystekniker':
        object_list = Consert.objects.filter(
            rigging__person__username=user.username).order_by(
            'tidspunkt').exclude(
            ~Q(tidspunkt__year='2018'))

        return render(request, 'app/lystekniker.html', {'conserts': object_list,
                                                        'rolle': rolle})
    else:
        return redirect('dashboard')

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
            for behov in consert.behov.all():
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
        return redirect('dashboard')

def bookingansvarlig(request):
    user = request.user
    if not user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig':
        current_consert = request.POST.get('scene-choices')
        if current_consert is not None and current_consert != 'alle':
            object_list = Consert.objects.order_by(
                'tidspunkt').exclude(
                ~Q(tidspunkt__year='2018'))
        else:
            object_list = Consert.objects.all().order_by(
                'tidspunkt').exclude(
                ~Q(tidspunkt__year='2018'))

        scene_list = Consert.objects.values('sceneNavn').distinct()

        return render(request,
                      'app/bookingansvarlig.html', {'conserts': object_list,
                                                             'rolle': rolle,
                                                             'sceneliste': scene_list,
                                                             'current_consert': current_consert})
    else:
        return redirect('dashboard')

def tidligere_konserter(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig':
        current_genre = request.POST.get('sjanger-choices')
        if current_genre is not None and current_genre != 'alle':
            concert_list = Consert.objects.filter(
                artist__sjanger=current_genre).exclude(
                tidspunkt__gte=datetime.now(),
                tidspunkt__year='2018')
        else:
            concert_list = Consert.objects.exclude(tidspunkt__gte=datetime.now(), tidspunkt__year='2018')

        sjanger_list = Artist.objects.values('sjanger').distinct()

        return render(request, 'app/tidligere_konserter.html', {'conserts': concert_list,
                                                                'rolle': rolle,
                                                                'sjangerliste': sjanger_list,
                                                                'current_genre': current_genre
                                                                })
    else:
        return redirect('dashboard')

def bookingsjef(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingsjef':

        # Static chosen dates for consistency
        start_date = datetime(2018, 6, 10)
        end_date = datetime(2018, 6, 16)

        # All concerts between chosen dates
        all_conserts = Consert.objects.filter(tidspunkt__range=(start_date, end_date))

        # Number ov avaiable dates where at least one scene is avaiable
        num_available = 7

        # Number of scenes that are booked that day
        num_booked_scenes = 0

        # Nested dict for each day:
        # weeklist { day1: {scene: concert_object, scene2... }, day2: {scene: ...}...}
        # Consists  of 7 days with each has a dict with 3 scene keys and eventually
        # containing None or Concert objects if booked
        week_list = {}

        curr_date = start_date
        # Go through days
        for day in range(7):

            week_list[day] = {}

            # Sets all scenes as none (not booked) for this day
            for scene in SCENER:
                week_list[day][scene] = None

            # For every concert that has a scene matching the scenes for this day
            # Replace None with concert
            # Add number of booked scenes by one
            for concert in all_conserts.filter(tidspunkt=curr_date).all():
                week_list[day][concert.sceneNavn] = concert
                num_booked_scenes += 1

            #For each day, if the day has 3 booked scenes means
            #it is booked for the current day and number of available is decreased by one day
            if num_booked_scenes == 3:
                num_available -= 1

            # Resets number of booked scenes for the next day
            num_booked_scenes = 0

            curr_date += timedelta(days=1)

        num_tilbud = Tilbud.objects.filter(godkjent_av_bookingsjef=True,
                                           sendt_av_ansvarlig=True,
                                           godkjent_av_manager=None).count()

        # Number of booked is 7 days minus number of avaiable
        num_booked = 7 - num_available

        return render(request, 'app/bookingsjef.html', {
                                                        'rolle': rolle,
                                                        'num_available': num_available,
                                                        'num_booked': num_booked,
                                                        'num_tilbud': num_tilbud,
                                                        'week_list': week_list
                                                        })
    else:
        return redirect('dashboard')


def manager(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'manager':

        all_conserts = Consert.objects.all().order_by('tidspunkt')
        artist_list = Artist.objects.filter(manager=user.profile).order_by('navn')
        conserts = []

        for consert in all_conserts:
            if consert.artist in artist_list:
                conserts.append(consert)

        return render(request, 'app/manager.html', {
                                                    'conserts': conserts,
                                                    'rolle': rolle
                                                    })
    else:
        return redirect('dashboard')

def legg_til_behov_manager(request, artist, concert_id):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'manager':
        consert = Consert.objects.get(id=concert_id)
        #To avoid spaces in url
        artist_slug = consert.artist.slug

        behov_form = LeggTilBehovForm()
        if request.method == 'POST':
            form = LeggTilBehovForm(request.POST)
            if form.is_valid():
                behov = form.save()
                consert.behov.add(behov)

        return render(request, 'app/legg_til_behov.html', {'behov_form': behov_form,
                                                           'rolle': rolle,
                                                           'consert': consert,
                                                           'artist_slug': artist_slug
                                                           })
    else:
        return redirect('dashboard')


def delete_behov_manager(request, artist, concert_id, behov_id):
    Behov.objects.filter(id=behov_id).delete()
    return redirect('legg_til_behov_manager', artist, concert_id)

def artist(request, navn):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'manager':
        band = Artist.objects.get(slug=navn)
        object_list = Consert.objects.filter(artist=band)

        return render(request, 'app/artist.html', {'conserts': object_list,
                                                   'rolle': rolle
                                                   })
    else:
        return render(request, 'dashboard', {'rolle': rolle})

def band_info(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig':
        object_list = Band_Info.objects.all()
        query = request.GET.get("q")
        if query:
            object_list = object_list.filter(band__icontains=query)

        context = {
            'bandInfo': object_list,
            'rolle': rolle
        }

        return render(request, 'app/bandSearch.html', context)
    else:
        return redirect('dashboard')

def tidligere_band(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig':
        object_list = Consert.objects.order_by(
            'artist__navn').exclude(
            tidspunkt__year='2018')

        query = request.GET.get("q")
        if query:
            object_list = object_list.filter(
                artist__navn__icontains=query).\
                exclude(tidspunkt__year='2018')

        context = {
            'conserts': object_list,
            'rolle': rolle,
        }

        return render(request, 'app/tidligere_band.html', context)
    else:
        return redirect('dashboard')

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
                messages.success(request, 'Tilbudet ble sendt')
            else:
                messages.error(request, 'Tilbudet ble ikke sendt, vennligst prøv igjen')

        form = RegistrerTilbudForm()
        return render(request, 'app/lag_tilbud.html', {'form': form,
                                                       'rolle': rolle
                                                       })
    else:
        return redirect('dashboard')


# Bookingsjef får liste over tilbud og kan godkjenne
def tilbud_liste_bookingsjef(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingsjef':
        object_list = Tilbud.objects.filter(godkjent_av_bookingsjef=None)
        num_tilbud = object_list.count()

        return render(request, 'app/tilbud_liste_bookingsjef.html', {'tilbuds': object_list,
                                                                     'rolle': rolle,
                                                                     'num_tilbud': num_tilbud
                                                                     })
    else:
        return redirect('dashboard')


def vurder_marked(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingsjef':
        current_scene = request.POST.get('booking-scene')
        current_genre = request.POST.get('booking-genre')
        if current_scene is not None and \
                        current_genre is not None and \
                        current_scene != 'alle' and current_genre == 'alle':
            concert_list = Consert.objects.filter(
                sceneNavn=current_scene).exclude(
                tidspunkt__gte=datetime.now())\
                .order_by('tidspunkt')
        elif current_scene is not None \
                and current_genre is not None\
                and current_scene == 'alle' \
                and current_genre != 'alle':
            concert_list = Consert.objects.filter(
                artist__sjanger=current_genre).exclude(
                tidspunkt__gte=datetime.now())\
                .order_by('tidspunkt')

        elif current_scene is not None and current_genre is not None\
                and current_scene != 'alle' \
                and current_genre != 'alle':
            concert_list = Consert.objects.filter(
                sceneNavn=current_scene, artist__sjanger=current_genre).exclude(
                tidspunkt__gte=datetime.now()).order_by('tidspunkt')
        else:
            concert_list = Consert.objects.exclude(
                tidspunkt__gte=datetime.now())\
                .order_by('tidspunkt')

        scene_list = Consert.objects.values('sceneNavn').distinct()
        genre_list = Artist.objects.values('sjanger').distinct()

        return render(request, 'app/vurder_marked.html',
                      {'conserts': concert_list, 'rolle': rolle,
                       'sceneliste': scene_list,
                       'sjangerliste': genre_list,
                       'current_scene': current_scene,
                       'current_genre': current_genre})
    else:
        return redirect('dashboard')



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

        return render(request, 'app/godkjenn_tilbud_bookingsjef.html',
                      {'tilbud': tilbud,
                       'form': form,
                       'rolle': rolle})
    else:
        return redirect('dashboard')


def generer_billettpris(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingsjef':

        consert_list = Consert.objects.all()
        for consert in consert_list:
            tilskuertall_total = consert.tilskuertall
            tilskuertall_snitt = 0.9*tilskuertall_total

            totale_kostnader = consert.kostnader
            totale_kostnader += 500*consert.behov.all().count()
            totale_kostnader += 2000*consert.rigging.all().count()

            if consert.sceneNavn == 'hallen':
                totale_kostnader += 15000
            elif consert.sceneNavn == 'storhallen':
                totale_kostnader += 20000
            else:
                totale_kostnader += 30000

            if tilskuertall_snitt <= 0.0:
                tilskuertall_snitt = 0.5 * tilskuertall_total

            if tilskuertall_snitt <= 0:
                pris = 0
            else:
                pris = math.ceil(((totale_kostnader+(tilskuertall_total*300)) / tilskuertall_snitt) * 1.2)

            if pris <= 350:
                pris = 350

            consert.billettpris = pris

        return render(request, 'app/generer_billettpris.html', {
                                                                'conserts': consert_list,
                                                                'rolle': rolle
                                                                })
    else:
        return redirect('dashboard')


#Bookingansvarlig får godkjent tilbud og sender videre
def tilbud_liste_bookingansvarlig(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig':
        tilbuds_liste = Tilbud.objects.all()

        return render(request,
                      'app/tilbud_liste_bookingansvarlig.html',
                      {'tilbuds_liste': tilbuds_liste,
                       'num_tilbud': tilbuds_liste.count(),
                       'rolle': rolle})
    else:
        return redirect('dashboard')

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

        return render(request, 'app/send_tilbud_bookingansvarlig.html',
                      {'tilbud': tilbud,
                       'form': form,
                       'rolle': rolle})
    else:
        return redirect('dashboard')


def tilbud_liste_manager(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'manager':

        artists_of_manager = Artist.objects.filter(manager=user.profile)

        #Alle tilbud
        all_tilbuds = Tilbud.objects.filter(godkjent_av_bookingsjef=True,
                                            sendt_av_ansvarlig=True,
                                            godkjent_av_manager=None)

        #Filtrerer ut tilbud til gitt manager
        manager_tilbud_list = all_tilbuds.exclude(~Q(artist__in=artists_of_manager))

        num_tilbud = len(manager_tilbud_list)

        return render(request, 'app/tilbud_liste_manager.html',
                      {'manager_tilbud_list': manager_tilbud_list,
                       'num_tilbud': num_tilbud,
                       'rolle': rolle})
    else:
        return redirect('dashboard')


def godkjenn_tilbud_manager(request, tilbud_id):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'manager':

        tilbud = Tilbud.objects.get(id=tilbud_id)
        form = GodkjennTilbudManagerForm(instance=tilbud)

        if request.method == 'POST':
            form = GodkjennTilbudManagerForm(request.POST, instance=tilbud)
            if form.is_valid():
                form.save()
                cd = form.cleaned_data
                #Accepted offer
                if cd['godkjent_av_manager'] == True:
                    Consert.objects.create(artist=tilbud.artist,
                                           tidspunkt=tilbud.tidspunkt,
                                           sceneNavn=tilbud.scene_navn,
                                           inntekter=tilbud.pris)

                return redirect('tilbud_liste_manager')

        return render(request, 'app/godkjenn_tilbud_manager.html', {'tilbud': tilbud,
                                                                    'form': form,
                                                                    'rolle': rolle
                                                                    })
    else:
        return redirect('dashboard')


def tilbud_detaljer(request, tilbud_id):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig' or \
                'bookingsjef' or \
                'manager':
        tilbud = Tilbud.objects.get(id=tilbud_id)

        return render(request, 'app/tilbud_detaljer.html',
                      {'tilbud': tilbud, 'rolle': rolle})
    else:
        return redirect('dashboard')
