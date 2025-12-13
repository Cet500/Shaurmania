from django.contrib import admin

from geodata.models import TimeZone


@admin.register( TimeZone )
class TimeZoneAdmin(admin.ModelAdmin):
	list_display    = [ 'tz', 'by_utc' ]
	list_filter     = [ 'shift' ]
	readonly_fields = [ 'tz', 'shift', 'by_utc' ]
	search_fields   = [ 'tz', 'shift' ]

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False
