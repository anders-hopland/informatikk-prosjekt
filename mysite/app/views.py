from django.shortcuts import render
from . models import Artist, Consert


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
    return render(request, 'app/dashboard.html', {'rolle': rolle})

def arrangor(request):
    user = request.user

    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'arrangor':
        object_list = Consert.objects.all().order_by('tidspunkt')

        return render(request, 'app/arrangor.html', {'conserts': object_list,  'rolle': rolle})
    else:
        return render(request, 'app/dashboard.html', {'rolle': rolle})

def lydtekniker(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'lydtekniker':
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/lydtekniker.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'app/dashboard.html', {'rolle': rolle})

def lystekniker(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'lystekniker':
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/lystekniker.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'app/dashboard.html', {'rolle': rolle})

def konsert(request, year, month, day, post_id):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'arrangor' or rolle == 'bookingansvarlig':
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
        return render(request, 'app/dashboard.html', {'rolle': rolle})

def detaljer_scener(request, navn):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'arrangor':
        object_list = Consert.objects.filter(sceneNavn=navn)
        return render(request, 'app/sceneDetaljer.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'app/dashboard.html', {'rolle': rolle})

def manager(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'manager':
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/manager.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'app/dashboard.html', {'rolle': rolle})

def bookingansvarlig(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig':
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/bookingansvarlig.html', {'conserts': object_list, 'rolle': rolle})
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
        return render(request, 'app/dashboard.html', {'rolle': rolle})

def scener(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    if rolle == 'arrangor':
        object_list = Consert.objects.values('sceneNavn').distinct()
        return render(request, 'app/scener.html', {'scener': object_list, 'rolle': rolle})
    return render(request, 'app/dashboard.html', {'rolle': rolle})
