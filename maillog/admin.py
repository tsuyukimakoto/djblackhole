from django.contrib import admin
from models import Attatchment, LoggedMail, RealAddress

class AttatchmentOptions(admin.ModelAdmin):
    pass

class LoggedMailOptions(admin.ModelAdmin):
    list_display = ('rcv', 'to_address', 'subject')
    ordering = ('-received_date',)

class RealAddressOptions(admin.ModelAdmin):
    list_display = ('email', 'suspend',)

admin.site.register(Attatchment, AttatchmentOptions)
admin.site.register(LoggedMail, LoggedMailOptions)
admin.site.register(RealAddress, RealAddressOptions)

