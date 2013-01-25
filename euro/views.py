# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from euro.models import Coins
from euro.models import Country

# Create your views here.
def coins(request):
    if 'country' in request.GET:
        coins = Coins.objects.filter(country__name = request.GET['country']).order_by('nominal')
        country = Country.objects.all().order_by('name')
	return render_to_response('coins.html',  {'coins': coins, 'query': request.GET['country'], 'country': country})
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)