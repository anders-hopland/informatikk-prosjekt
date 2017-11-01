from django.contrib import admin
from . models import Extend_user, Rigging, Consert, Artist, Tilbud, Behov, Band_Info

# Register your models here.
admin.site.register(Extend_user)
admin.site.register(Rigging)
admin.site.register(Consert)
admin.site.register(Tilbud)
admin.site.register(Artist)
admin.site.register(Behov)
admin.site.register(Band_Info)