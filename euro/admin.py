# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from euro.models import Country, Nominal, Coins, CoinGroup
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
#from django.contrib.admin.options import changelist_view

class CoinsForm(forms.ModelForm):
    coin_group = forms.ModelMultipleChoiceField(queryset = CoinGroup.objects.all())

    class Meta:
        model = Coins

    def __init__(self, *args, **kwargs):
        print "Error __init__ 1"
        try:
            coin = kwargs['instance']
        except:
            super(CoinsForm, self).__init__(*args, **kwargs)
        return

        super(CoinsForm, self).__init__(*args, **kwargs)

        try:
            print "Error __init__ 2"
            self.fields['coin_group'].queryset = Country.objects.filter(name = unicode(coin.country))[0].coin_group.all()
        except:
            print "Error __init__ 3"
            self.fields['coin_group'].queryset = CoinGroup.objects.all()
        
class CoinsCountry(admin.ModelAdmin):
    ordering = ('name',)


class DecadeBornListFilter(SimpleListFilter):
    title = (u'Группы')

    parameter_name = 'group__id__exact'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        for q in qs:
            yield (str(q.id), _(q.group_name))

    def queryset(self, request, queryset):
        if 'group__id__exact' in request.GET:
            return queryset.filter(coin_group__id = request.GET['group__id__exact'])
        return queryset

class CoinsAdmin(admin.ModelAdmin):
    form = CoinsForm
#    list_filter = ('country', 'coin_group',)
    list_filter = ('country', DecadeBornListFilter,)
    ordering = ('country', 'nominal',)

    def get_queryset(self, request):
        if 'country__id__exact' in request.GET:
            return Country.objects.filter(id = request.GET['country__id__exact'])[0].coin_group.all()
        return CoinGroup.objects.all()


class CoinGroupAdmin(admin.ModelAdmin):
    ordering = ('group_name',)


admin.site.register(Country, CoinsCountry)
admin.site.register(Nominal)
admin.site.register(Coins, CoinsAdmin)
admin.site.register(CoinGroup, CoinGroupAdmin)