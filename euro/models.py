# ~*~ coding: utf-8 ~*~

from django.db import models
from django.contrib.auth.models import User

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
        ordering = ['group_name', ]


# описание страны в которой находиться монетка
class Country(models.Model):
    name = models.CharField(max_length=30)
    coin_group = models.ManyToManyField(CoinGroup, blank=True)

    class Meta:
        verbose_name = u'страна'
        verbose_name_plural = verbose_name
        ordering = ['name', ]

    def __unicode__(self):
        return self.name


# описание монеки
class Coins(models.Model):
    country = models.ForeignKey(Country, verbose_name=u'Страна')
    nominal = models.ForeignKey(Nominal, verbose_name=u'Номинал')
    image = models.ImageField(upload_to='usa/territory',
                              verbose_name=u'Картинка')  # где лежат фотографии монет
    coin_group = models.ManyToManyField(CoinGroup, verbose_name=u'Группы',
                                        blank=True)  # группа к которой относиться монета
    coin_owner = models.ManyToManyField(User, verbose_name=u'Владельцы', blank=True)  # кто владеет монетой
    year = models.IntegerField(blank=True, verbose_name=u'Год выпуска', null=True)  # год выпуска монеты
    description = models.TextField(blank=True, verbose_name=u'Описание', null=True)  # описание монеты

    def __unicode__(self):
        description = u'%s - %s' % (unicode(self.country), unicode(self.nominal))
        description += u' - %s' % unicode(self.description) if self.description else ''
        return description

    class Meta:
        verbose_name = u'Монеты'
        verbose_name_plural = verbose_name
        ordering = ['country', ]


