from django.conf.urls import url
from app.views import dashboard

urlpatterns = [
    url(r'^$', dashboard, name='dashboard'),
]

