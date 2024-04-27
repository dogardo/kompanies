from django.contrib import admin
from .models import *

# Basit bir şekilde admin paneline kaydetme
admin.site.register(BusinessLine)
admin.site.register(Country)
admin.site.register(tx_ID)

class ArchivedItemAdmin(admin.ModelAdmin):
    list_display = ('name','url',"id", 'display_password')
    search_fields = ('name','url',"id")
    def display_password(self, obj):
        return '*****'
    display_password.short_description = 'Password'  # Bu satır metoda özel bir başlık tanımlar.

admin.site.register(ArchivedItem, ArchivedItemAdmin)

admin.site.register(tableBusiness)
admin.site.register(pointGroup)

