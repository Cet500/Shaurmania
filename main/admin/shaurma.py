from django.contrib import admin
from django.utils.safestring import mark_safe
from main.models import Shaurma, ShaurmaCategory, ShaurmaImage


@admin.register(Shaurma)
class ShaurmaAdmin(admin.ModelAdmin):
	list_display       = [ 'id', 'name', 'get_picture', 'compound', 'category', 'get_energy_value', 'get_price', 'get_weight', 'created_at' ]
	list_display_links = [ 'name' ]
	list_filter        = [ 'created_at' ]

	def get_picture( self, obj ):
		if obj.picture:
			return mark_safe( f'<img src="{obj.picture.url}" width="100" />' )
		else:
			return mark_safe( f'<b>нет</b>' )

	get_picture.short_description = 'Изображение'

	def get_energy_value( self, obj ):
		return f'{obj.calories} ккал   {obj.proteins} / {obj.fats} / {obj.carbohydrates}'

	get_energy_value.short_description = 'Данные КБЖУ'

	def get_price( self, obj ):
		return f'{obj.price} ₽'

	get_price.short_description = 'Цена в ₽'

	def get_weight( self, obj ):
		return f'{obj.weight} гр'

	get_weight.short_description = 'Вес в гр'


class ShaurmaInline( admin.TabularInline  ):
	model = Shaurma
	extra = 0
	fields = [ 'name', 'price', 'weight', 'calories', 'is_available', 'created_at' ]
	readonly_fields = [ 'name', 'created_at' ]
	show_change_link = True
	can_delete = False
	can_add = False


@admin.register( ShaurmaCategory )
class ShaurmaCategoryAdmin( admin.ModelAdmin ):
	list_display       = [ 'name', 'shaurma_count', 'description', 'created_at' ]
	list_display_links = [ 'name' ]
	list_filter        = [ 'created_at' ]

	inlines = [ ShaurmaInline ]

	def shaurma_count( self, obj ):
		return obj.shaurma_set.count()

	shaurma_count.short_description = "Размер"


@admin.register( ShaurmaImage )
class ShaurmaImageAdmin( admin.ModelAdmin ):
	list_display       = [ 'shaurma', 'caption', 'get_image', 'created_at' ]
	list_display_links = [ 'shaurma' ]
	list_filter        = [ 'shaurma', 'created_at' ]

	def get_image( self, obj ):
		if obj.image:
			return mark_safe( f'<img src="{obj.image.url}" width="200" />' )
		else:
			return mark_safe( f'<b>нет</b>' )

	get_image.short_description = 'Изображение'
