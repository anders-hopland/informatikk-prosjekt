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

def konsert(request, year, month, day, post_id):
    user = request.user
    if not request.user.is_authenticated():
        return render(request, 'app/dashboard.html', {})

    rolle = user.profile.role
    if rolle == 'arrangor':
        object_list = Consert.objects.filter(id = post_id)
        return render(request, 'app/konsert.html', {'conserts': object_list, 'rolle': rolle})
    else:
        return render(request, 'registration/login.html', {})
