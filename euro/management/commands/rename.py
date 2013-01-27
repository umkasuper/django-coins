from django.core.management.base import NoArgsCommand
from django.template import Template, Context
from django.conf import settings
from euro.models import Coins


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for coin in Coins.objects.all():
            #print coin.image.path.split('/')
            print coin.image.path.split('/')[-1]
            coin.image = '/img/euro/' + coin.image.path.split('/')[-1]
            coin.save()
