# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response
from euro.models import Coins, Country

class countryCoins():
    coins_group = []
    country_name= ""

    def __init__(self, country_name):
        self.country_name = country_name
        self.coins_group = []

    def add_coin_group(self, coin_group):
        self.coins_group.append(coin_group)

class groupCoin():

    def __init__(self, coins_group, coins_group_name):
        self.coins_group = coins_group
        self.coins_group_name = coins_group_name


def euro_memorable(request):
    if 'country' in request.GET:
        if request.GET['country'] == "all":
            request_country_list = Country.objects.all().values_list('name', flat=True)
        else:
            request_country_list = request.GET['country'].split(",")

        # список всех евро стран
        country_descriptions = []
        country = Country.objects.filter(coin_group__group_name__in=['euro']).order_by('name'). distinct()
        for place in country:
            country_description = countryCoins(place.name)
            country_descriptions.append(country_description)

        return render_to_response('euro_memorable.html',  {'country_descriptions':country_descriptions, 'request': request})
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

def euro(request):
    if 'country' in request.GET:

        if request.GET['country'] == "all":
            request_country_list = Country.objects.all().values_list('name', flat=True)
        else:
            request_country_list = request.GET['country'].split(",")
        grouped_country = []

        # список всех стран, вместе с типами монет
        country_descriptions = []
        country = Country.objects.filter(coin_group__group_name__in=['euro', 'normal']).order_by('name'). distinct()
        for place in country:
            country_description = countryCoins(place.name)

            types = place.coin_group.all().exclude(group_name__in=['euro', 'normal'])
            for type in types:
                country_description.add_coin_group(groupCoin(None, type.group_name))
            country_descriptions.append(country_description)

        for request_country in request_country_list:
            group_country = countryCoins(request_country)
            # получили все монеты этой страны
            coins_of_country = Coins.objects.filter(country__name = request_country)

            if coins_of_country:
                if 'type' in request.GET:
                    type_of_coins = Country.objects.filter(name = request_country)[0].coin_group.all().filter(group_name=request.GET['type'])
                else:
                    type_of_coins = Country.objects.filter(name = request_country)[0].coin_group.all().exclude(group_name__in=['euro', 'normal'])

                # есть типы кроме euro, и стандарт (есть ли другие выпуски?)
                if type_of_coins:
                    for coins_group_name in type_of_coins.values_list('group_name', flat=True):
                        coins = coins_of_country.filter(coin_group__group_name = coins_group_name).order_by('coin_group', 'nominal')
                        group_country.add_coin_group(groupCoin(coins, coins_group_name))
                else:
                    group_country.add_coin_group(groupCoin(coins_of_country.order_by('nominal'), ""))

            grouped_country.append(group_country)
            # 'query': request_country,
        return render_to_response('euro.html',  {'country_descriptions':country_descriptions, 'request': request,  'grouped_country': grouped_country})
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

def usa(request):
    return render_to_response('usa.html',  {'request': request})

def russia(request):
    return render_to_response('russia.html',  {'request': request})
