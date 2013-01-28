# ~*~ coding: utf-8 ~*~

from django.db import models

# Create your models here.



# описание номинала монетки
class Nominal(models.Model):
    value = models.CharField(max_length=10)

    class Meta:
        verbose_name = u'Номиналы'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.value

# группировка монеток по признакам
class CoinGroup(models.Model):
    group_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.group_name

    class Meta:
        verbose_name = u'Группы'
        verbose_name_plural = verbose_name
        ordering = ['group_name',]

# описание страны в которой находиться монетка
class Country(models.Model):
    name = models.CharField(max_length=30)
    coin_group = models.ManyToManyField(CoinGroup)

    class Meta:
        verbose_name = u'Страны'
        verbose_name_plural = verbose_name
        ordering = ['name',]

    def __unicode__(self):
        return self.name

# описание монеки
class Coins(models.Model):
    country = models.ForeignKey(Country)
    nominal = models.ForeignKey(Nominal)
    image = models.ImageField(upload_to='img/euro')
    coin_group = models.ManyToManyField(CoinGroup)

    def __unicode__(self):
        return u'%s - %s' % (unicode(self.country), unicode(self.nominal))

    class Meta:
        verbose_name = u'Монеты'
        verbose_name_plural = verbose_name
        ordering = ['country',]


