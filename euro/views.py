# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from euro.models import Coins
from euro.models import Country

# Create your views here.
class groupCoin():

    def __init__(self, coins_group, coins_group_name):
        self.coins_group = coins_group
        self.coins_group_name = coins_group_name


def coins(request):
    if request.user.is_authenticated():
        if 'country' in request.GET:
                print request.user.username

                request_country = request.GET['country']
                country = Country.objects.filter(coin_group__group_name__in=['euro', 'normal']).order_by('name'). distinct()
                coins_of_country = Coins.objects.filter(country__name = request_country)

                if coins_of_country:
                    type_of_coins = Country.objects.filter(name = request_country)[0].coin_group.all().exclude(group_name__in=['euro', 'normal'])

                    coins_group = []
                    # есть типы кроме euro, и стандарт (есть ли другие выпуски?)
                    if type_of_coins:
                        for coins_group_name in type_of_coins.values_list('group_name', flat=True):
                            coins = coins_of_country.filter(coin_group__group_name = coins_group_name).order_by('coin_group', 'nominal')
                            coins_group.append(groupCoin(coins, coins_group_name.split()[-1]))
                    else:
                        coins_group.append(groupCoin(coins_of_country.order_by('nominal'), "euro"))

                    return render_to_response('coins.html',  {'request': request, 'query': request_country, 'country': country, 'coins_group': coins_group})
                else:
                    message = 'Coins country %s not found.' % request.GET['country']
        else:
                message = 'You submitted an empty form.'
    else:
        message = 'Please authenticated.'
    return HttpResponse(message)