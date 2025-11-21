from django.contrib import admin
from main.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display       = [ 'name', 'text', 'get_stars', 'shaurma', 'date' ]
	list_display_links = [ 'name' ]
	list_filter        = [ 'stars', 'date' ]

	def get_stars( self, obj ):
		return f'{obj.stars} {'★' * obj.stars}'

	get_stars.short_description = 'Оценка'
