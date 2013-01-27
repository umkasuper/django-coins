# ~*~ coding: utf-8 ~*~

from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = u'Страны'
        verbose_name_plural = verbose_name
        ordering = ['name',]

    def __unicode__(self):
        return self.name


class Nominal(models.Model):
    value = models.CharField(max_length=10)

    class Meta:
        verbose_name = u'Номиналы'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.value

class Coins(models.Model):
    country = models.ForeignKey(Country)
    nominal = models.ForeignKey(Nominal)
    image = models.ImageField(upload_to='img/euro')

    def __unicode__(self):
        return u'%s - %s' % (unicode(self.country), unicode(self.nominal))

    class Meta:
        verbose_name = u'Монеты'
        verbose_name_plural = verbose_name
        ordering = ['country',]
