# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from euro.models import Country, Nominal, Coins, CoinGroup
from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import widgets
from django.conf import settings
from django.utils.safestring import mark_safe
#from django.contrib.admin.options import changelist_view


class CountrySelector(forms.Select):

    def __init__(self, attrs=None, choices=()):
        super(CountrySelector, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        return super(CountrySelector, self).render(name, value, attrs, choices)
#        return rendered + mark_safe(u'''<script type="text/javascript"></script>''')


class CoinsForm(forms.ModelForm):
#    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(), label=u"Страны")
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=CountrySelector(), label=u"Страны")

    coin_group = forms.ModelMultipleChoiceField(queryset=CoinGroup.objects.all(),
                                                widget=widgets.FilteredSelectMultiple(u'Группы', False),
                                                label=Coins._meta.get_field_by_name('coin_group')[0].verbose_name)


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
            self.fields['coin_group'].queryset = Country.objects.filter(name=unicode(coin.country))[0].coin_group.all()
        except:
            print "Error __init__ 3"
            self.fields['coin_group'].queryset = CoinGroup.objects.all()


class CoinsCountry(admin.ModelAdmin):
    ordering = ('name',)


class DecadeBornListFilter(SimpleListFilter):
    title = u'Группы'

    parameter_name = 'group__id__exact'

    def lookups(self, request, model_admin):
        # выбираем группы выбранной страны
        if 'country__id__exact' in request.GET:
            qs = Country.objects.filter(id=request.GET['country__id__exact'])[0].coin_group.all()
        else: # выбираемвсе группы
            qs = CoinGroup.objects.all()
            
        for q in qs:
            yield (str(q.id), _(q.group_name))

    def queryset(self, request, queryset):
        if 'group__id__exact' in request.GET:
            return queryset.filter(coin_group__id=request.GET['group__id__exact'])
        return queryset


class CoinsAdmin(admin.ModelAdmin):
    form = CoinsForm
    list_filter = ('country', DecadeBornListFilter,)
    filter_horizontal = ('coin_owner', 'coin_group',)
    ordering = ('country', 'nominal',)
    #ordering = ('country', 'coins',)
    def get_queryset(self, request):
        return Coins.objects.all()

    def save_model(self, request, obj, form, change):
        obj.save(coin_group=form.cleaned_data['coin_group'].values_list('group_name', flat=True))


class CoinGroupAdmin(admin.ModelAdmin):
    ordering = ('group_name',)


admin.site.register(Country, CoinsCountry)
admin.site.register(Nominal)
admin.site.register(Coins, CoinsAdmin)
admin.site.register(CoinGroup, CoinGroupAdmin)