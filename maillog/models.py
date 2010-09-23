from django.db import models
from django.utils.translation import ugettext_noop as _
import datetime


class RealAddress(models.Model) :
    """Relay received mail if 'rcpt address' exists here
    """
    email   = models.EmailField(_(u'Email Address'), blank=False)
    suspend = models.BooleanField(_(u'Suspend Flag'), default=False, help_text=_(u'Treat this address as fake one when this flag is true'))

    def __unicode__(self):
        return self.email

date_format = '%m-%d %H:%M:%S'

class LoggedMail(models.Model) :
    from_address   = models.EmailField(_(u'Sender address'), blank=True)
    to_address     = models.EmailField(_(u'Recipient address'), blank=False)
    received_date  = models.DateTimeField(_(u'Received'), blank=False, auto_now_add=True)
    charset        = models.CharField(_(u'Mime-Encoding'), max_length=100, blank=True)
    raw_header     = models.TextField(_(u'Raw Header'), blank=True)
    header         = models.TextField(_(u'Decoded Header'), blank=True)
    subject        = models.TextField(_(u'Subject'), blank=True)
    raw_body       = models.TextField(_(u'Raw Body'), blank=True)
    body           = models.TextField(_(u'Decoded Body'), blank=True)

    def __unicode__(self):
        return u'%s' % (self.subject)

    def rcv(self):
        return self.received_date.strftime(date_format)


class Attatchment(models.Model) :
    loggedMail  = models.ForeignKey(LoggedMail)
    origin_name = models.CharField(_(u'Original File Name'), max_length=200)
    file        = models.FileField(_(u'file'), upload_to='attatch')

    def __unicode__(self):
        return self.origin_name

