from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import os
import sys

class Command(BaseCommand):
    help = "Starts a blackhole smtp server for development."
    def handle(self, port='', *args, **options):
        import asyncore
        import server
        local_port = 8888
        if args:
            raise CommandError('Usage is blackholesmtpd %s' % self.args)
        if not port:
            port = '25'
        if not port.isdigit():
            raise CommandError("%r is not a valid port number." % port)
        
        svr = server.BlackHoleSmtp(("localhost", int(port)), ('localhost', local_port))
        try:
            asyncore.loop()
        except KeyboardInterrupt:
            pass
        except Exception, e:
            sys.stderr.write(self.style.ERROR("Error: %s" % str(e)) + '\n')
            sys.exit(0)
