from django.shortcuts import render
from . models import Artist

def dashboard(request):
    object_list = Artist.objects.all()
    return render(request, 'app/dashboard.html', {'artists' : object_list})