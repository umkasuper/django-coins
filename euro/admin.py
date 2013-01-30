# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from euro.models import Country, Nominal, Coins, CoinGroup


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
        
class CoinsCounrty(admin.ModelAdmin):
    ordering = ('name',)

class CoinsAdmin(admin.ModelAdmin):
    form = CoinsForm
    list_filter = ('country',)
    ordering = ('country', 'nominal',)


class CoinGroupAdmin(admin.ModelAdmin):
    ordering = ('group_name',)


admin.site.register(Country, CoinsCounrty)
admin.site.register(Nominal)
admin.site.register(Coins, CoinsAdmin)
admin.site.register(CoinGroup, CoinGroupAdmin)