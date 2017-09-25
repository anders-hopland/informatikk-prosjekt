from django.shortcuts import render
from . models import Artist, Konsert

def dashboard(request):
    object_list = Artist.objects.all()
    return render(request, 'app/dashboard.html', {})

def arrangor(request):
    user = request.user

    if user.profile.role == 'arrangor':
        object_list = Konsert.objects.all();
        return render(request, 'app/arrangor.html', {'konserts' : object_list})
    else:
        return render(request, 'app/dashboard.html', {})

def lydtekniker(request):
    user = request.user

    if user.profile.role == 'arrangor':
        object_list = Konsert.objects.filter(rigging__person__username=user.username)
        return render(request, 'app/lydtekniker.html', {'konserts': object_list})
    else:
        return render(request, 'app/dashboard.html', {})