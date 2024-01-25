from django.contrib import admin
from . models import *

admin.site.register(Kunde)
admin.site.register(Artikel)
admin.site.register(Bestellung)
admin.site.register(BestellteArtikell)
admin.site.register(Adresse)
