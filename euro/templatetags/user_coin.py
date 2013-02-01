# ~*~ coding: utf-8 ~*~

from django import template

register = template.Library()

def user_have_coin(user, coin):
    return u"Есть" if coin.coin_owner.filter(username = user.username) else None


register.filter('user_have_coin', user_have_coin)

