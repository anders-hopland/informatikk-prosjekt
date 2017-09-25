from django.conf.urls import url, include
from app.views import dashboard, arrangor, lydtekniker
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^arrangor/$', arrangor, name='arrangor'),
    url(r'^lydtekniker/$', lydtekniker, name='lydtekniker'),

    #login logout
    url('^', include('django.contrib.auth.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^$', dashboard, name='dashboard'),
]

