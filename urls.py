from django.conf.urls.defaults import *
from django.contrib import databrowse
from django.views.static import serve
from django.conf import settings
import os

from django.contrib import admin
admin.autodiscover()

from maillog.models import LoggedMail

databrowse.site.register(LoggedMail)

urlpatterns = patterns('',
    (r'^attach/(?P<path>.*)', serve, dict(document_root=os.path.join(settings.BASE_DIR, 'attach'), show_indexes=True)),
    (r'^admin/(.*)', admin.site.root),
    (r'^databrowse/(.*)', databrowse.site.root),
)
