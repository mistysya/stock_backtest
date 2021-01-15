from django.db import models
from django.contrib import admin

# Create your models here.
class StockInfo(models.Model):
    stock_symbol = models.CharField(max_length=15)
    stock_name = models.CharField(max_length=10)

class StockDailyInfo(models.Model):
    stock_symbol = models.CharField(max_length=15)
    exchange_date = models.DateField()

    volume = models.FloatField(default=None, blank=True, null=True)
    open_price = models.FloatField(default=None, blank=True, null=True)
    close_price = models.FloatField(default=None, blank=True, null=True)
    high_price = models.FloatField(default=None, blank=True, null=True)
    low_price = models.FloatField(default=None, blank=True, null=True)

    pe = models.FloatField(default=None, blank=True, null=True)
    pb = models.FloatField(default=None, blank=True, null=True)
    dividend = models.FloatField(default=None, blank=True, null=True)

    foreign_invest = models.BigIntegerField(default=None, blank=True, null=True)
    invest_trust = models.BigIntegerField(default=None, blank=True, null=True)
    dealer = models.BigIntegerField(default=None, blank=True, null=True)
    investors  = models.BigIntegerField(default=None, blank=True, null=True)

    ma5 = models.FloatField(default=None, blank=True, null=True)
    ma10 = models.FloatField(default=None, blank=True, null=True)
    ma20 = models.FloatField(default=None, blank=True, null=True)
    ma60 = models.FloatField(default=None, blank=True, null=True)
    ma120 = models.FloatField(default=None, blank=True, null=True)

class StockMonthInfo(models.Model):
    stock_symbol = models.CharField(max_length=15)
    exchange_date = models.DateField()
    revenue = models.BigIntegerField(default=None, blank=True, null=True)

class StockSeasonInfo(models.Model):
    stock_symbol = models.CharField(max_length=15)
    exchange_date = models.DateField(default=None, blank=True, null=True)
    gross_margin = models.FloatField(default=None, blank=True, null=True)

class StockDailyInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'exchange_date', 'stock_symbol', 'close_price', 'ma5', 'ma10', 'investors')

class StockInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock_symbol', 'stock_name')

class StockMonthInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'exchange_date', 'stock_symbol', 'revenue')