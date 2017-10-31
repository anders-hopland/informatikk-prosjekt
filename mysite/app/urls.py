from django.conf.urls import url, include

from . views import arrangor, lydtekniker, dashboard, lystekniker, artist, lag_tilbud, godkjenn_tilbud_bookingsjef
from . views import manager, bookingansvarlig, bookingsjef, konsert, tilbud_liste_bookingsjef, band_info

from django.contrib.auth import views as auth_views


'''
INFO
urlpatterns is a list of different urls. Each url has 3
arguments, a regular expression for trying to match the
url the user has typed in, a view it will call to render
the page given that the url is correct and a name, which makes
it easier to refer to the url in our html using jinja
'''


urlpatterns = [
    url(r'^artist/(?P<navn>\w+)$', artist, name='artist'),
    url(r'^arrangor/$', arrangor, name='arrangor'),
    url(r'^lydtekniker/$', lydtekniker, name='lydtekniker'),
    url(r'^lystekniker/$', lystekniker, name='lystekniker'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^konsert/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post_id>\d+)/$', konsert, name='konsert'),
    url(r'^manager/$', manager, name='manager'),
    url(r'^bookingansvarlig/$', bookingansvarlig, name='bookingansvarlig'),
    url(r'^bookingsjef/$', bookingsjef, name='bookingsjef'),
    url(r'^band_info/$', band_info , name='band_info'),
    url(r'^lag_tilbud/$', lag_tilbud, name='lag_tilbud'),
    url(r'^tilbudsliste_bookingsjef/$', tilbud_liste_bookingsjef, name='tilbud_liste_bookingsjef'),
    url(r'^godkjenn_tilbud_bookingsjef/(?P<tilbud_id>\d+)/$', godkjenn_tilbud_bookingsjef, name='godkjenn_tilbud_bookingsjef'),

    #login logout
    url('^', include('django.contrib.auth.urls')),
    url(r'^login/', auth_views.login, name='login'),
    url(r'^logout/', auth_views.logout, name='logout'),

    url(r'^$', auth_views.login, name='login'),
]

