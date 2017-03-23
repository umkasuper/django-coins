# ~*~ coding: utf-8 ~*~

from django import template
import re
import unidecode
from django.conf import settings

register = template.Library()

def user_have_coin(user, coin):
    return u"Есть" if coin.coin_owner.filter(username = user.username) else None


register.filter('user_have_coin', user_have_coin)

def user_have_coin_present(user, coin):
    return 'present' if coin.coin_owner.filter(username = user.username) else 'absent'


@register.simple_tag
def get_id_name(country_name, group_name):
    return '%s%s%s' % (group_name if group_name else "", '-' if group_name else "", country_name)

@register.simple_tag
def user_coins_info(request, coin, country_name, group_name):
    id_name = get_id_name(country_name, group_name)
    present = user_have_coin_present(request.user, coin) if request.user.is_authenticated else ""
    div_class_row = u'<div class="row" style="background-image:url(%s);" id="%s_%s">' % (coin.image.url, id_name, present)
    if request.user.is_authenticated():
        div_class_present = u'<div class="present" style="background-image:url(%s); width: 25px; height: 22px;" id="%s_%d_%s_%s"> </div>' % ('/media/check.png' if present == 'present' else '/media/uncheck.png', coin.id, coin.year if coin.year else 0, id_name, 'absent' if present == 'present' else 'present')
    else:
        div_class_present = ''
    print(div_class_row + div_class_present)
    return div_class_row + div_class_present

@register.simple_tag
def country_from_path(request):
    return request.get_full_path().split('/')[-1]

@register.simple_tag
def media_root():
    return getattr(settings, 'MEDIA_ROOT', '/')

def u_slugify(str):
    str = unidecode.unidecode(str).lower()
    return re.sub(r'\W+','-',str)

register.filter('u_slugify', u_slugify)