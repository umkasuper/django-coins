from django.contrib import admin
from euro.models import Country, Nominal, Coins

class CoinsCounrty(admin.ModelAdmin):
    ordering = ('name',)

class CoinsAdmin(admin.ModelAdmin):
    list_filter = ('country',)
    ordering = ('country', 'nominal',)

admin.site.register(Country, CoinsCounrty)
admin.site.register(Nominal)
admin.site.register(Coins, CoinsAdmin)
