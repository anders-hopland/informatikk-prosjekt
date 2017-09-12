from django.contrib import admin
from app.models import extend_user, rigging, Konsert, Artist, Tilbud

# Register your models here.
admin.site.register(extend_user)
admin.site.register(rigging)
admin.site.register(Konsert)
admin.site.register(Tilbud)
admin.site.register(Artist)
