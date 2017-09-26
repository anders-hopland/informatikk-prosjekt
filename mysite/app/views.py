from django.shortcuts import render
from . models import Artist, Consert

def dashboard(request):
    object_list = Artist.objects.all()
    return render(request, 'app/dashboard.html', {})

def arrangor(request):
    user = request.user

    if not request.user.is_authenticated():
        return render(request, 'app/dashboard.html', {})

    if user.profile.role == 'arrangor':
        object_list = Consert.objects.all();
        return render(request, 'app/arrangor.html', {'conserts' : object_list})
    else:
        return render(request, 'app/dashboard.html', {})

def lydtekniker(request):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'app/dashboard.html', {})

    if user.profile.role == 'arrangor':
        object_list = Consert.objects.filter(rigging__person__username=user.username)
        return render(request, 'app/lydtekniker.html', {'conserts': object_list})
    else:
        return render(request, 'app/dashboard.html', {})
