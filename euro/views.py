# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from euro.models import Coins, Country

class countryCoins():
    coins_group = []
    country_name = ""

    def __init__(self, country_name):
        self.country_name = country_name
        self.coins_group = []

    def add_coin_group(self, coin_group):
        self.coins_group.append(coin_group)

class groupCoin():

    def __init__(self, coins_group, coins_group_name):
        self.coins_group = coins_group
        self.coins_group_name = coins_group_name


def coins(request):
    if request.user.is_authenticated():
        if 'country' in request.GET:
            print request.user.username

            request_country_list = request.GET['country'].split(",")
            grouped_country = []

            country = Country.objects.filter(coin_group__group_name__in=['euro', 'normal']).order_by('name'). distinct()
            for request_country in request_country_list:
                group_country = countryCoins(request_country)
                coins_of_country = Coins.objects.filter(country__name = request_country)

                if coins_of_country:
                    type_of_coins = Country.objects.filter(name = request_country)[0].coin_group.all().exclude(group_name__in=['euro', 'normal'])

                    # есть типы кроме euro, и стандарт (есть ли другие выпуски?)
                    if type_of_coins:
                        for coins_group_name in type_of_coins.values_list('group_name', flat=True):
                            coins = coins_of_country.filter(coin_group__group_name = coins_group_name).order_by('coin_group', 'nominal')
                            group_country.add_coin_group(groupCoin(coins, coins_group_name.split()[-1]))
                    else:
                        group_country.add_coin_group(groupCoin(coins_of_country.order_by('nominal'), ""))

                grouped_country.append(group_country)

            return render_to_response('coins.html',  {'request': request, 'query': request_country, 'country': country, 'grouped_country': grouped_country})
#                    else:
#                        message = 'Coins country %s not found.' % request.GET['country']
        else:
                message = 'You submitted an empty form.'
    else:
        message = 'Please authenticated.'
    return HttpResponse(message)