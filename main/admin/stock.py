from django.contrib import admin
from django.utils.safestring import mark_safe
from main.models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
	list_display = [ 'name', 'get_image', 'short_text', 'display_categories', 'get_discount', 'get_dates' ]

	def get_image( self, obj ):
		if obj.image:
			return mark_safe( f'<img src="{obj.image.url}" width="100" />' )
		else:
			return mark_safe( f'<b>нет</b>' )

	get_image.short_description = 'Изображение'

	def display_categories( self, obj ):
		return ", ".join( [category.name for category in obj.categories.all()] )

	display_categories.short_description = 'Категории'

	def get_discount( self, obj ):
		return f'{obj.discount} %'

	get_discount.short_description = 'Скидка'

	def get_dates( self, obj ):
		if obj.date_start == obj.date_end:
			return f'{obj.date_end}'
		else:
			return f'{obj.date_start} - {obj.date_end}'

	get_dates.short_description = 'Время акции'
