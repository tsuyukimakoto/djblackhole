import os
import email
import mimetypes
import smtpd
from logging import debug
from datetime import datetime
from email import message_from_string
from email.Header import decode_header, make_header
from email.Utils import decode_rfc2231

from maillog.models import RealAddress, LoggedMail, Attatchment

from django.conf import settings

ATTACH_DIR = os.path.join(settings.MEDIA_ROOT, 'attach')

class BlackHoleSmtp(smtpd.PureProxy):
    real_address_list = None

    def process_message(self, remoteHosts, mailfrom, rcpttos, data):
        if not BlackHoleSmtp.real_address_list:
            BlackHoleSmtp.real_address_list = set([a.email for a in RealAddress.objects.filter(suspend__exact=False)])
        recipients = ','.join(rcpttos)
        real_addresses = BlackHoleSmtp.real_address_list & set(rcpttos) #TODO check rcpttos data
        for real_address in real_addresses :
            smtpd.PureProxy.process_message(self, remoteHosts, mailfrom, [real_address], data) #check real_address data
            #smtpd.PureProxy.process_message(self, remoteHosts, mailfrom, rcpttos, data)
            debug('send email to: %s',(real_address,))
        msg = message_from_string(data)
        log = LoggedMail(from_address=mailfrom, to_address=recipients)
        charset = 'latin1'

        log.raw_header =  '\n'.join([ '%s:%s' % (key, msg.get(key)) for key in msg.keys()])
        header = ''
        for key in msg.keys():
            value, type = decode_header(msg.get(key))[0]
            if not type:
                value = unicode(value)
            else:
                value = unicode(value, type)
                charset = type
            header += '%s:%s(mime:%s)\n' % (key, value, type)
            if key == 'Subject':
                log.subject = value
        log.header = header
        log.charset = charset
        log.save()

        file_name_base = 'msg_%07d_' % log.id
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get_content_maintype() == 'text':
                log.raw_body += part.get_payload(decode=0)
                log.body += unicode(part.get_payload(decode=1), charset)
                log.save()
                continue
            file_name = part.get_filename()
            if not file_name:
                ext = ".bin"
                if hasattr(part, 'get_type'):
                    ext = mimetypes.guess_extension(part.get_type())
                file_name = 'part-%03d%s' % (file_count, ext)
            at = log.attatchment_set.create(origin_name=file_name)
            file_name = file_name_base + file_name
            file = part.get_payload(decode=1)
            f = open(os.path.join(ATTACH_DIR, file_name), 'w')
            f.write(file)
            f.close()
            at.file = u'attach/%s' % file_name
            at.save()
