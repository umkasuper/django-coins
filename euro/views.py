# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from euro.models import Coins
from euro.models import Country

# Create your views here.
def coins(request):
    if request.user.is_authenticated():
        if 'country' in request.GET:
                print request.user.username

                country = Country.objects.all().order_by('name')
                coins_of_country = Coins.objects.filter(country__name = request.GET['country'])

                if coins_of_country:
                    type_of_coins = Country.objects.filter(name = request.GET['country'])[0].coin_group.all().exclude(group_name__in=['euro', 'normal'])

                    # есть типы кроме euro, и стандарт
                    if type_of_coins:
                        coins = coins_of_country.filter(coin_group__group_name__in=type_of_coins.values_list('group_name', flat=True)).order_by('coin_group', 'nominal')
                    else:
                        coins = coins_of_country.order_by('nominal')

                    return render_to_response('coins.html',  {'coins': coins, 'query': request.GET['country'], 'country': country})
                else:
                    message = 'Coins country %s not found.' % request.GET['country']
        else:
                message = 'You submitted an empty form.'
    else:
        message = 'Please authenticated.'
    return HttpResponse(message)