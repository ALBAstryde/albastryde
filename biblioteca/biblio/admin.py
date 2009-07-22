from django.contrib import admin
from models import Autor, Editorial, Biblioteca


class BiblioAdmin(admin.ModelAdmin):
    list_display = ('name','autor','fecha','attachment')
    list_filter = ('autor','fecha','organizacion')
    ordering = ('fecha',)
    search_fields = ('name', 'attachment','autor')

admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Biblioteca, BiblioAdmin)
