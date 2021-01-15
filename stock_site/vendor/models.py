from django.db import models
from django.contrib import admin

from django.utils.translation import gettext_lazy as _

# Create your models here.
class Vendor(models.Model):
    vendor_name = models.CharField(max_length=20)
    store_name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.vendor_name

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
	list_display = ('id', 'vendor_name', 'store_name', 'phone_number', 'address') 

class Food(models.Model):
    food_name = models.CharField(max_length=30)
    price_name = models.DecimalField(max_digits=3, decimal_places=0)
    food_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return self.food_name

class Morethanfifty(admin.SimpleListFilter):

	title = _('price')
	parameter_name = 'compareprice' # url最先要接的參數

	def lookups(self, request, model_admin):
		return (
			('>50',_('>50')), # 前方對應下方'>50'(也就是url的request)，第二個對應到admin顯示的文字
			('<=50',_('<=50')),
		)
    # 定義查詢時的過濾條件
	def queryset(self, request, queryset):
		if self.value() == '>50':
			return queryset.filter(price_name__gt=50)
		if self.value() == '<=50':
			return queryset.filter(price_name__lte=50)

class Testfifty(admin.SimpleListFilter):

	title = _('test')
	parameter_name = 'testcompare' # url最先要接的參數

	def lookups(self, request, model_admin):
		return (
			('>40',_('>40')), # 前方對應下方'>50'(也就是url的request)，第二個對應到admin顯示的文字
			('<=40',_('<=40')),
		)
    # 定義查詢時的過濾條件
	def queryset(self, request, queryset):
		if self.value() == '>40':
			return queryset.filter(price_name__gt=40)
		if self.value() == '<=40':
			return queryset.filter(price_name__lte=40)

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Food._meta.fields] # It's fine but there is warning...
    list_filter = (Morethanfifty, Testfifty, 'food_name')
    #fields = ['price_name']
    search_fields = ('food_name','price_name')
    ordering = ('price_name',) 