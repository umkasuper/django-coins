# ~*~ coding: utf-8 ~*~

import json
from euro.models import Coins, Country
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from operator import methodcaller
from datetime import datetime
#logger = logging.getLogger(__name__)

class Description:
    def __init__(self):
        pass

    def json(self):
        return vars(self)

class CountryDescription(Description):
    img = None
    name = ""
    all_coins = 0
    have_coins = -1

    def __init__(self, img, name, all_coins, have_coins):
        self.img = img
        self.name = name
        self.all_coins = all_coins
        self.have_coins = have_coins
        Description.__init__(self)


@csrf_exempt
def api_v1_euro_list_countries(request):
    if request.method == 'POST':
        country_descriptions = []
        request_country_list = Country.objects.filter(coin_group__group_name__in=['euro']).filter(coin_group__group_name__in=['memorable']).distinct().order_by('name')
        coins = Coins.objects.filter(coin_group__group_name__in=['euro']).filter(coin_group__group_name__in=['memorable'])
        all_coins = 0
        all_have_coins = 0 if request.user.is_authenticated() else -1
        for request_country in request_country_list:
            # сколько всего монет этой страны
            coins_of_country = coins.filter(country__name=request_country.name).order_by('year')
            # сколько монет этой страны есть у пользователя
            coins_of_country_user = -1
            if request.user.is_authenticated():
                 coins_of_country_user = len(coins_of_country.filter(coin_owner__username=request.user.username))
            country_descriptions.append(CountryDescription(request_country.flag.url, request_country.name, len(coins_of_country), coins_of_country_user))
            all_coins += len(coins_of_country)
            all_have_coins += coins_of_country_user if request.user.is_authenticated() else 0

        country_descriptions.insert(0, CountryDescription("/media/flags/euro.png", "all", all_coins, all_have_coins))

        return HttpResponse(json.dumps(country_descriptions, default=methodcaller("json")), content_type="application/json")
    return HttpResponse("error only POST")


class YearDescription(Description):
    name = ""
    all_coins = 0
    have_coins = -1
 
    def __init__(self, name, all_coins, have_coins):
        self.name = name
        self.all_coins = all_coins
        self.have_coins = have_coins
        Description.__init__(self)

@csrf_exempt
def api_v1_euro_list_years(request):
    if request.method == 'POST':
        country_descriptions = []
        coins = Coins.objects.filter(coin_group__group_name__in=['euro']).filter(coin_group__group_name__in=['memorable'])
        for year in xrange(2004, datetime.now().year + 1):
            coins_of_year = coins.filter(year=year).order_by('country__name')
            coins_of_year_user = -1
            if request.user.is_authenticated():
                coins_of_year_user = len(coins_of_year.filter(coin_owner__username=request.user.username))
            country_descriptions.append(YearDescription(str(year), len(coins_of_year), coins_of_year_user))

        return HttpResponse(json.dumps(country_descriptions, default=methodcaller("json")), content_type="application/json")
    return HttpResponse("error only POST")

class CoinDescription(Description):
    def __init__(self, img, year, country, flag, description, have, key):
        self.img = img
        self.year = str(year)
        self.country = country
        self.flag = flag
        self.description = description
        self.have = have
        self.key = key
        Description.__init__(self)

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
            is_have =  True if coin.coin_owner.all().filter(username=request.user.username) else False
            coins_answer.append(CoinDescription(coin.image.url, coin.year, coin.country.name, coin.country.flag.url, coin.description, is_have, coin.id))

        return HttpResponse(json.dumps(coins_answer, default=methodcaller("json")), content_type="application/json")

    return HttpResponse("error only POST")

@csrf_exempt
def api_v1_euro_save(request):

    if request.method == 'POST':
        jdata = json.loads(request.body)
        print(jdata['id'], jdata['have'])

        # получем id пользователя
        user = User.objects.filter(username=request.user.username)
        # нашли такого пользователя
        result = "ok"
        if user:
            coin = Coins.objects.filter(id=int(jdata['id']))
            # нашли монеты  у нужным id
            if coin:
                if jdata['have']:
                    try:
                        coin[0].coin_owner.add(user[0].id)
                    except:
                        result = u"bad add"
                else:
                    try:
                        coin[0].coin_owner.remove(user[0].id)
                    except:
                        result = u"bad remove"
            else:
                result = u"coin not found"
        else:
            result = u"user not found"

        return HttpResponse(json.dumps({"result": result}), content_type="application/json")

    return HttpResponse("error only POST")
