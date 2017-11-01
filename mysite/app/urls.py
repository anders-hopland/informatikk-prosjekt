from django.conf.urls import url, include

from . views import arrangor, lydtekniker, dashboard, lystekniker, artist
from . views import legg_til_behov_manager, lag_tilbud, godkjenn_tilbud_bookingsjef, generer_billettpris
from . views import manager, bookingansvarlig, bookingsjef, konsert
from . views import tidligere_konserter, tilbud_liste_bookingsjef, band_info, delete_behov_manager, tidligere_band, vurder_marked
from . views import tilbud_liste_bookingansvarlig, send_tilbud_bookingansvarlig, tilbud_liste_manager

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
    url(r'^artist/(?P<navn>\w+)$',
        artist,
        name='artist'),

    url(r'^arrangor/$',
        arrangor,
        name='arrangor'),

    url(r'^lydtekniker/$',
        lydtekniker,
        name='lydtekniker'),

    url(r'^lystekniker/$',
        lystekniker,
        name='lystekniker'),

    url(r'^dashboard/$',
        dashboard,
        name='dashboard'),

    url(r'^konsert/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post_id>\d+)/$',
        konsert,
        name='konsert'),

    url(r'^bookingansvarlig/tidligere_konserter/$',
        tidligere_konserter,
        name='tidligere_konserter'),

    url(r'^manager/$',
        manager,
        name='manager'),

    url(r'^legg_til_behov_manager/(?P<artist>\w+)/(?P<concert_id>\d+)/$',
        legg_til_behov_manager,
        name='legg_til_behov_manager'),

    url (r'^delete_behov_manager/(?P<artist>\w+)/(?P<concert_id>\d+)/(?P<behov_id>\d+)/$',
         delete_behov_manager,
         name='delete_behov_manager'),

    url(r'^bookingansvarlig/$',
        bookingansvarlig,
        name='bookingansvarlig'),

    url(r'^bookingsjef/$',
        bookingsjef,
        name='bookingsjef'),

    url(r'^bookingsjef/generer_billettpris/$',
        generer_billettpris,
        name='generer_billettpris'),

    url(r'^bookingsjef/vurder_marked/$',
        vurder_marked,
        name='vurder_marked'),

    url(r'^band_info/$',
        band_info,
        name='band_info'),

    url(r'^lag_tilbud/$',
        lag_tilbud,
        name='lag_tilbud'),

    url(r'^tilbudsliste_bookingsjef/$',
        tilbud_liste_bookingsjef,
        name='tilbud_liste_bookingsjef'),

    url(r'^tilbudsliste_bookingansvarlig/$',
        tilbud_liste_bookingansvarlig,
        name='tilbud_liste_bookingansvarlig'),

    url(r'^godkjenn_tilbud_bookingsjef/(?P<tilbud_id>\d+)/$',
        godkjenn_tilbud_bookingsjef,
        name='godkjenn_tilbud_bookingsjef'),

    url(r'^send_tilbud_bookingansvarlig/(?P<tilbud_id>\d+)/$',
        send_tilbud_bookingansvarlig,
        name='send_tilbud_bookingansvarlig'),

    url(r'^tilbudsliste_manager/$',
        tilbud_liste_manager,
        name='tilbud_liste_manager'),

    url(r'^tidligere_band/$',
        tidligere_band,
        name='tidligere_band'),

    #login logout
    url('^',
        include('django.contrib.auth.urls')),

    url(r'^login/',
        auth_views.login,
        name='login'),

    url(r'^logout/',
        auth_views.logout,
        name='logout'),

    url(r'^$',
        auth_views.login,
        name='login'),
]