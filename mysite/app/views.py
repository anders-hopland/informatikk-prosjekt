from django.shortcuts import render
from . models import Artist, Konsert

def dashboard(request):
    object_list = Artist.objects.all()
    return render(request, 'app/dashboard.html', {'artists' : object_list})

def arrangor(request):
    object_list = Konsert.objects.all();
    return render(request, 'app/arrangor.html', {'konserts' : object_list})