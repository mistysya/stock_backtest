from django.contrib import admin

from .models import StockInfo, StockDailyInfo, StockMonthInfo, StockSeasonInfo, StockInfoAdmin, StockDailyInfoAdmin, StockMonthInfoAdmin

# Register your models here.
admin.site.register(StockInfo, StockInfoAdmin)
admin.site.register(StockDailyInfo, StockDailyInfoAdmin)
admin.site.register(StockMonthInfo, StockMonthInfoAdmin)
admin.site.register(StockSeasonInfo)