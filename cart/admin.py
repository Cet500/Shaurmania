from django.contrib import admin
from .models import Order, Cart, Promocode


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_code', 'user', 'shaurma', 'quantity', 'line_total', 'date']
    list_filter = ['date', 'is_demo_payment']
    search_fields = ['order_code', 'user__username', 'shaurma__name']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'item', 'quanity', 'updated_at')
    list_filter = ('user',)
    search_fields = ('user__username', 'item__name', 'session_key')


@admin.register( Promocode )
class PromocodeAdmin( admin.ModelAdmin ):
    list_display = [ 'code_name', 'code_uuid', 'duration', 'discount', 'date_add', 'date_end' ]
    list_filter = [ 'date_add', 'date_end' ]
