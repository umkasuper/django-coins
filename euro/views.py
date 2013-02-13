# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from euro.models import Coins, Country
from django.contrib.auth.models import User

"""
Класс опимывающий выборку по страны
"""
class countryCoins():

    coins_group = []   # группы монет
    country_name= ""   # название страны

    def __init__(self, country_name):
        self.country_name = country_name
        self.coins_group = []

    def add_coin_group(self, coin_group):
        self.coins_group.append(coin_group)


"""
Оисание группы монент название группы (например год) и перечень монет для отображения
"""
class groupCoin():

    def __init__(self, coins_group, coins_group_name):
        self.coins_group = coins_group
        self.coins_group_name = coins_group_name

"""
Обработка запроса на получеие юбилейных euro монет
"""
def memorable(request, country, selectors):
    #if 'country' in request.GET:
    if country:
        if country == "all":
            request_country_list = Country.objects.all().values_list('name', flat=True)
        else:
            request_country_list = [country]

        # список всех евро стран
        country_descriptions = []
        country = Country.objects.filter(coin_group__group_name__in=selectors).order_by('name').distinct()
        for place in country:
            country_description = countryCoins(place.name)
            country_descriptions.append(country_description)

        # получили все монеты этой страны
        grouped_country = []
        for request_country in request_country_list:
            group_country = countryCoins(request_country)
            coins_of_country = Coins.objects.filter(country__name = request_country).order_by('coin_group', 'nominal')
            for selector in selectors:
                coins_of_country = coins_of_country.filter(coin_group__group_name = selector)
            coins_of_country = coins_of_country.order_by('coin_group', 'nominal')

            grouped_country.append(group_country)


        return render_to_response('memorable.html',  {'coins': coins_of_country, 'country_descriptions':country_descriptions, 'request': request})
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

"""
Обработка запроса для отображени euro монет
"""
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

            types = place.coin_group.all().exclude(group_name__in=['euro', 'normal', 'memorable'])
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
                    type_of_coins = Country.objects.filter(name = request_country)[0].coin_group.all().exclude(group_name__in=['euro', 'normal', 'memorable'])

                # есть типы кроме euro, и стандарт (есть ли другие выпуски?)
                if type_of_coins:
                    for coins_group_name in type_of_coins.values_list('group_name', flat=True):
                        coins = coins_of_country.filter(coin_group__group_name = coins_group_name).order_by('coin_group', 'nominal')
                        group_country.add_coin_group(groupCoin(coins, coins_group_name))
                else:
                    group_country.add_coin_group(groupCoin(coins_of_country.exclude(coin_group__group_name = 'memorable').order_by('nominal'), ""))

            grouped_country.append(group_country)
            # 'query': request_country,
        return render_to_response('euro.html',  {'country_descriptions':country_descriptions, 'request': request,  'grouped_country': grouped_country})
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

# обработка запроса выдачи страницы монет США
def usa(request):
    return render_to_response('usa.html',  {'request': request})

"""
Обработка запроса выдачи страницы с монетыми России
"""
def russia(request):
    return render_to_response('russia.html',  {'request': request})

"""
 Обработка POST запроса на запись, удаление монеты в колекцию
 """
@csrf_exempt
def set_coins(request):
    if ('id' in request.POST) and ('operation' in request.POST):
        # получем id пользователя
        user = User.objects.filter(username = request.user.username)
        # нашли такого пользователя
        if user:
            coin = Coins.objects.filter(id = int(request.POST['id']))
            # нашли монеты  у нужным id
            if coin:
                if request.POST['operation'] == "add":
                    try:
                        coin[0].coin_owner.add(user[0].id)
                    except:
                        return HttpResponse(u"bad add")

                if request.POST['operation'] == "remove":
                    try:
                        coin[0].coin_owner.remove(user[0].id)
                    except:
                        return HttpResponse(u"bad remove")
            return HttpResponse(u"ok")
        else:
            return HttpResponse(u"user not found")

    return HttpResponse(u"need params")

