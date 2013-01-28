from django.contrib import admin
from euro.models import Country, Nominal, Coins, CoinGroup

class CoinsCounrty(admin.ModelAdmin):
    ordering = ('name',)

class CoinsAdmin(admin.ModelAdmin):
    list_filter = ('country',)
    ordering = ('country', 'nominal',)

class CoinGroupAdmin(admin.ModelAdmin):
    ordering = ('group_name',)

admin.site.register(Country, CoinsCounrty)
admin.site.register(Nominal)
admin.site.register(Coins, CoinsAdmin)
admin.site.register(CoinGroup, CoinGroupAdmin)