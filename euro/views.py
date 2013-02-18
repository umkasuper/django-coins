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
    all_coins_country = 0
    have_coins_country = 0

    def __init__(self, country_name, all_coins_country, have_coins_country):
        self.country_name = country_name
        self.all_coins_country = all_coins_country
        self.have_coins_country = have_coins_country
        self.coins_group = []


    def add_coin_group(self, coin_group):
        self.coins_group.append(coin_group)


"""
Оисание группы монент название группы (например год) и перечень монет для отображения
"""
class groupCoin():
    coins_group = []
    coins_group_name = ""
    all_coins_group = 0
    have_coins_group = 0


    def __init__(self, coins_group, coins_group_name, all_coins_group, have_coins_group):
        self.coins_group = coins_group
        self.coins_group_name = coins_group_name
        self.all_coins_group = all_coins_group
        self.have_coins_group = have_coins_group

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

        # список соответсвующих selectors
        country_descriptions = []
        country = Country.objects.all()

        # отбираем все монеты соответствующие selectors
        coins_selectors = Coins.objects.all()
        for selector in selectors:
            country = country.filter(coin_group__group_name = selector)
            coins_selectors = coins_selectors.filter(coin_group__group_name = selector)
        country = country.order_by('name').distinct()

        grouped_country = []
        for place in country:
            # сколько всего монет этой страны
            coins_of_country = coins_selectors.filter(country__name = place.name).order_by('year')
            # сколько монет этой страны есть у пользователя
            coins_of_country_user = coins_of_country.filter(coin_owner__username = request.user.username)

            if place.name in request_country_list: # если эта страна среди запршеных
                country = countryCoins(place.name, len(coins_of_country), len(coins_of_country_user))
                country.add_coin_group(groupCoin(coins_of_country, place.name, 0, 0))
                grouped_country.append(country) # добавляем ее

            country_description = countryCoins(place.name, len(coins_of_country), len(coins_of_country_user))
            country_descriptions.append(country_description)

#        # получили все монеты этой страны
#        for request_country in request_country_list:
#            coins_of_country = coins_selectors.filter(country__name = request_country).order_by('-year')

        return render_to_response('memorable.html',  {'country': grouped_country, 'country_descriptions':country_descriptions, 'request': request})
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

            # сколько всего монет этой страны
            coins_of_country = Coins.objects.filter(country__name = place.name).exclude(coin_group__group_name__in=['memorable'])
            # сколько монет этой страны есть у пользователя
            coins_of_country_user = coins_of_country.filter(coin_owner__username = request.user.username)

            # создаем описатель для страны
            country_description = countryCoins(place.name, len(coins_of_country), len(coins_of_country_user))

            # находим какие группы монет етсь в этой стране кроме euro, normal, memorable
            types = place.coin_group.all().exclude(group_name__in=['euro', 'normal', 'memorable'])
            for type in types:
                # находим все монеты нужного типа
                coins_of_country_type = coins_of_country.filter(coin_group__group_name = type.group_name)
                # находим монеты нужного типа умеющиеся у пользователя
                coins_of_country_user_type = coins_of_country_user.filter(coin_group__group_name = type.group_name)

                country_description.add_coin_group(groupCoin(None, type.group_name, len(coins_of_country_type), len(coins_of_country_user_type)))

            country_descriptions.append(country_description)

            del coins_of_country
            del coins_of_country_user

        for request_country in request_country_list:
            group_country = countryCoins(request_country, 0, 0)
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
                        group_country.add_coin_group(groupCoin(coins, coins_group_name, 0, 0))
                else:
                    group_country.add_coin_group(groupCoin(coins_of_country.exclude(coin_group__group_name = 'memorable').order_by('nominal'), "", 0, 0))

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

