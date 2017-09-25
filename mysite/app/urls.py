from django.conf.urls import url
from app.views import dashboard, arrangor, lydtekniker

urlpatterns = [
    url(r'^arrangor/$', arrangor, name='arrangor'),
    url(r'^lydtekniker/$', lydtekniker, name='lydtekniker'),
    url(r'^$', dashboard, name='dashboard'),
]

