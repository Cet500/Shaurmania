from django.contrib import admin
from django.utils.safestring import mark_safe
from main.models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	list_display       = [ 'name', 'description', 'planet', 'country', 'city', 'address', 'get_picture', 'timeline', 'created_at' ]
	list_display_links = [ 'name' ]
	list_filter        = [ 'planet', 'country', 'timeline', 'created_at']

	def get_picture( self, obj ):
		if obj.picture:
			return mark_safe( f'<img src="{obj.picture.url}" width="200" />' )
		else:
			return mark_safe( f'<b>нет</b>' )

	get_picture.short_description = 'Изображение'
