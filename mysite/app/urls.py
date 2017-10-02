from django.conf.urls import url, include
from app.views import arrangor, lydtekniker, dashboard, lystekniker
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^arrangor/$', arrangor, name='arrangor'),
    url(r'^lydtekniker/$', lydtekniker, name='lydtekniker'),
    url(r'^lystekniker/$', lystekniker, name='lystekniker'),
    url(r'^dashboard/$', dashboard, name='dashboard'),

    #login logout
    url('^', include('django.contrib.auth.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^$', auth_views.login, name='login'),
]

