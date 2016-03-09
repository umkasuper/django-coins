# ~*~ coding: utf-8 ~*~

import json
from euro.models import Coins, Country
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from operator import methodcaller
from datetime import datetime
#logger = logging.getLogger(__name__)

class country:
    name = ""
    all_coins = 0
    have_coins = -1
    def __init__(self, name, all_coins, have_coins):
        self.name = name
        self.all_coins = all_coins
        self.have_coins = have_coins

    def json(self):
        return vars(self)


@csrf_exempt
def api_v1_euro_list_countries(request):
    if request.method == 'POST':
        country_descriptions = []
        request_country_list = list(Country.objects.filter(coin_group__group_name__in=['euro']).filter(coin_group__group_name__in=['memorable']).distinct().order_by('name').values_list('name', flat=True))
        coins = Coins.objects.filter(coin_group__group_name__in=['euro']).filter(coin_group__group_name__in=['memorable'])
        all_coins = 0
        all_have_coins = -1
        for country_name in request_country_list:
            # сколько всего монет этой страны
            coins_of_country = coins.filter(country__name=country_name).order_by('year')
            # сколько монет этой страны есть у пользователя
            coins_of_country_user = -1
            if request.user.is_authenticated():
                 coins_of_country_user = len(coins_of_country.filter(coin_owner__username=request.user.username))
            country_descriptions.append(country(country_name, len(coins_of_country), coins_of_country_user))
            all_coins += len(coins_of_country)
            all_have_coins += coins_of_country_user if request.user.is_authenticated() else 0

        country_descriptions.insert(0, country("all", all_coins, all_have_coins))

        return HttpResponse(json.dumps(country_descriptions, default=methodcaller("json")), content_type="application/json")
    return HttpResponse("error only POST")

@csrf_exempt
def api_v1_euro_list_years(request):
    if request.method == 'POST':
        country_descriptions = []
        coins = Coins.objects.filter(coin_group__group_name__in=['euro']).filter(coin_group__group_name__in=['memorable'])
        for year in xrange(2004, datetime.now().year + 1):
            coins_of_year = coins.filter(year=year).order_by('country__name')
            print "%d %d" % (year, len(coins_of_year))
            coins_of_year_user = -1
            if request.user.is_authenticated():
                coins_of_year_user = len(coins_of_year.filter(coin_owner__username=request.user.username))
            country_descriptions.append(country(str(year), len(coins_of_year), coins_of_year_user))

        return HttpResponse(json.dumps(country_descriptions, default=methodcaller("json")), content_type="application/json")
    return HttpResponse("error only POST")

class ccoin:
    def __init__(self, img, year, country, description, have, key):
        self.img = img
        self.year = str(year)
        self.country = country
        self.description = description
        self.have = have
        self.key = key

    def json(self):
        return vars(self)

@csrf_exempt
def api_v1_euro_what(request):

    if request.method == 'POST':
        jdata = json.loads(request.body)
        if jdata['type'] == 'country':  #по стране
             coins = Coins.objects.filter(coin_group__group_name__in=['euro']).filter(coin_group__group_name__in=['memorable'])
             if jdata['what'] != 'all':
                 coins = coins.filter(country__name=jdata['what'])

        if jdata['type'] == 'year':  #по году
             coins = Coins.objects.filter(coin_group__group_name__in=['euro']).filter(coin_group__group_name__in=['memorable'])
             coins = coins.filter(year=jdata['what'])

        coins_answer = []
        coins = coins.order_by('year')
        for coin in coins:
            coins_answer.append(ccoin(coin.image.url, coin.year, "", coin.description, True, coin.id))

        #   coin = ccoin("media/euro/2013_Vatican_memorable_2.png", "2013", u"Ватикан", u"Даже не знаю что это", True, 0)
        #    coins.append(coin)

        #    coin = ccoin("media/euro/2013_Spain_memorable_2.png", "2013", u"Испания", u"что то из Испании", False, 1)
        #    coins.append(coin)

        #    coin = ccoin("media/euro/2013_Slovenia_memorable_2.png", "2013", u"Словения", u"что то из Словении", True, 2)
        #    coins.append(coin)

        return HttpResponse(json.dumps(coins_answer, default=methodcaller("json")), content_type="application/json")
       
    return HttpResponse("error only POST")
       