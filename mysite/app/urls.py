from django.conf.urls import url
from app.views import dashboard, arrangor

urlpatterns = [
    url(r'^arrangor/$', arrangor, name='arrangor'),
    url(r'^$', dashboard, name='dashboard'),
]

