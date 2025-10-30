from django.contrib import admin
from .models import Order, Cart, Promocode


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'shaurma', 'date']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quanity')  # было 'shaurma' — заменено на 'item' и 'quanity' (как в модели)
    list_filter = ('user',)
    search_fields = ('user__username', 'item__name')


@admin.register( Promocode )
class PromocodeAdmin( admin.ModelAdmin ):
    list_display = [ 'code_name', 'code_uuid', 'duration', 'discount', 'date_add', 'date_end' ]
    list_filter = [ 'date_add', 'date_end' ]
