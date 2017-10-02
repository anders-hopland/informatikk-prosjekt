from django.conf.urls import url, include
from app.views import arrangor, lydtekniker, dashboard, lystekniker, konsert
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^arrangor/$', arrangor, name='arrangor'),
    url(r'^lydtekniker/$', lydtekniker, name='lydtekniker'),
    url(r'^lystekniker/$', lystekniker, name='lystekniker'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^konsert/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post_id>\d+)/$', konsert, name='konsert'),

    #login logout
    url('^', include('django.contrib.auth.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^$', auth_views.login, name='login'),
]

