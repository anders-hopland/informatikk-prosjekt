from django.shortcuts import render
from . models import Artist, Consert

def dashboard(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'registration/login.html', {})

    rolle = user.profile.role
    return render(request, 'app/dashboard.html', {'rolle': rolle})

def arrangor(request):
    user = request.user

    if not request.user.is_authenticated():
        return render(request, 'app/dashboard.html', {})

    rolle = user.profile.role
    if rolle == 'arrangor':
        object_list = Consert.objects.all().order_by('tidspunkt')
        print(rolle)
        return render(request, 'app/arrangor.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'registration/login.html', {})

def lydtekniker(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'app/dashboard.html', {})

    rolle = user.profile.role
    if rolle == 'tekniker':
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/lydtekniker.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'registration/login.html', {})

def lystekniker(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'app/dashboard.html', {})

    rolle = user.profile.role
    if rolle == 'tekniker':
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/lystekniker.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'registration/login.html', {})

def manager(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'app/manager.html', {})

    rolle = user.profile.role
    if rolle == 'manager':
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/manager.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'registration/login.html', {})

def bookingansvarlig(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'app/manager.html', {})

    rolle = user.profile.role
    if rolle == 'bookingansvarlig':
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/bookingansvarlig.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'registration/login.html', {})

def bookingsjef(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'app/bookingsjef.html', {})

    rolle = user.profile.role
    if rolle == 'bookingsjef':
        object_list = Consert.objects.filter(rigging__person__username=user.username).order_by('tidspunkt')
        return render(request, 'app/manager.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'registration/login.html', {})

