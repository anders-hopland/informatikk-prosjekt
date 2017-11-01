from django.shortcuts import render, redirect

from django.db.models import Count
from . models import Artist, Consert, Tilbud, Behov, Band_Info
from datetime import datetime

from . forms import LeggTilBehovForm, SendTilbudBookingAnsvarligForm
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
            object_list = Consert.objects.filter(sceneNavn=current_consert).order_by('tidspunkt').exclude(~Q(tidspunkt__year='2017'))
        else:
            object_list = Consert.objects.all().order_by('tidspunkt').exclude(~Q(tidspunkt__year='2017'))

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
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt').exclude(~Q(tidspunkt__year='2017'))
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
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt').exclude(~Q(tidspunkt__year='2017'))
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
            object_list = Consert.objects.order_by('tidspunkt').exclude(~Q(tidspunkt__year='2017'))
        else:
            object_list = Consert.objects.all().order_by('tidspunkt').exclude(~Q(tidspunkt__year='2017'))

        scene_list = Consert.objects.values('sceneNavn').distinct()

        return render(request, 'app/bookingansvarlig.html', {'conserts': object_list,
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
            concert_list = Consert.objects.filter(artist__sjanger=current_genre).exclude(tidspunkt__gte=datetime.now(), tidspunkt__year='2017')
        else:
            concert_list = Consert.objects.exclude(tidspunkt__gte=datetime.now(), tidspunkt__year='2017')

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
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/manager.html', {'conserts': object_list,
                                                    'rolle': rolle
                                                    })
    else:
        return redirect('dashboard')


def manager(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'manager':

        all_conserts = Consert.objects.all().exclude(tidspunkt__lte=datetime.now()).order_by('tidspunkt')
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
        object_list = Consert.objects.order_by('artist__navn').exclude(tidspunkt__year='2017')
        query = request.GET.get("q")
        if query:
            object_list = object_list.filter(artist__navn__icontains=query).exclude(tidspunkt__year='2017')

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
                redirect('dashboard')
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
        object_list = Tilbud.objects.filter(godkjent_av_bookingssjef=None)
        # Num_conserts = Consert.objects.filter(tidspunkt__year=2017).count()

        return render(request, 'app/tilbud_liste_bookingsjef.html', {'tilbuds': object_list,
                                                                     'rolle': rolle
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
        if current_scene is not None and current_genre is not None and current_scene != 'alle' and current_genre == 'alle':
            concert_list = Consert.objects.filter(sceneNavn=current_scene).exclude(tidspunkt__gte=datetime.now()).order_by('tidspunkt')
        elif current_scene is not None and current_genre is not None and current_scene == 'alle' and current_genre != 'alle':
            concert_list = Consert.objects.filter(artist__sjanger=current_genre).exclude(tidspunkt__gte=datetime.now()).order_by('tidspunkt')
        elif current_scene is not None and current_genre is not None and current_scene != 'alle' and current_genre != 'alle':
            concert_list = Consert.objects.filter(sceneNavn=current_scene, artist__sjanger=current_genre).exclude(tidspunkt__gte=datetime.now()).order_by('tidspunkt')
        else:
            concert_list = Consert.objects.exclude(tidspunkt__gte=datetime.now()).order_by('tidspunkt')

        scene_list = Consert.objects.values('sceneNavn').distinct()
        genre_list = Artist.objects.values('sjanger').distinct()

        return render(request, 'app/vurder_marked.html',
                      {'conserts': concert_list, 'rolle': rolle, 'sceneliste': scene_list, 'sjangerliste': genre_list,
                       'current_scene': current_scene, 'current_genre': current_genre})
    else:
        return render(request, 'app/dashboard.html', {'rolle': rolle})



def godkjenn_tilbud_bookingsjef(request, artist, tilbud_id):
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

        return render(request, 'app/godkjenn_tilbud_bookingsjef.html', {'tilbud': tilbud,
                                                                        'form': form,
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
        object_list = Tilbud.objects.filter(godkjent_av_bookingssjef=True, sendt_av_ansvarlig=None)
        #num_conserts = Consert.objects.filter(tidspunkt__year=2017).count()

        return render(request, 'app/tilbud_liste_bookingansvarlig.html', {'tilbuds': object_list, 'rolle': rolle})
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

        return render(request, 'app/send_tilbud_bookingansvarlig.html', {'tilbud': tilbud, 'form': form, 'rolle': rolle})
    else:
        return redirect('dashboard')


'''
###############
Bookingmanager mailbox
###############
'''

def tilbud_liste_manager(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'manager':
        object_list = Tilbud.objects.filter(godkjent_av_bookingssjef=True, sendt_av_ansvarlig=True)
        num_tilbud = Tilbud.objects.filter(godkjent_av_bookingssjef=True, sendt_av_ansvarlig=True).count()

        return render(request, 'app/tilbud_liste_manager.html', {'tilbuds': object_list, "antall_tilbud": num_tilbud, 'rolle': rolle})
    else:
        return redirect('dashboard')
