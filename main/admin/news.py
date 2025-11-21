from django.contrib import admin
from django.utils.safestring import mark_safe
from main.models import News


@admin.register( News )
class NewsAdmin( admin.ModelAdmin ):
	list_display       = [ 'title', 'is_shown', 'short_text', 'get_picture', 'created_at' ]
	list_display_links = [ 'title' ]
	list_filter        = [ 'created_at' ]

	def get_picture( self, obj ):
		if obj.picture:
			return mark_safe( f'<img src="{obj.picture.url}" width="200" />' )
		else:
			return mark_safe( f'<b>нет</b>' )

	get_picture.short_description = 'Изображение'
