# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from euro.models import Coins

# Create your views here.
class coins_object():

    def __init__(self, name, value):
        self.name = name
        self.value = value

def coins(request):
    if 'country' in request.GET:
#        message = 'You searched for %s' % request.GET['country']
#        key_name = ['1c', '2c', '5c', '10c', '20c', '50c', '1€', '2€']
        coins = Coins.objects.filter(country__name = request.GET['country']).order_by('nominal')
	return render_to_response('coins.html',  {'coins': coins, 'query': request.GET['country']})
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)