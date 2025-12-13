import zoneinfo
from datetime import datetime
from django.core.management.base import BaseCommand
from geodata.models import TimeZone


class Command( BaseCommand ):
	def handle( self, *args, **options ):
		now = datetime.now()

		for tz_key in sorted( zoneinfo.available_timezones() ):
			tz = zoneinfo.ZoneInfo( tz_key )
			offset = tz.utcoffset( now )
			shift_hours = int( offset.total_seconds() / 3600 )

			TimeZone.objects.update_or_create(
				tz = tz_key,
				defaults = { 'shift': shift_hours }
			)

		self.stdout.write( self.style.SUCCESS( 'Таймзоны загружены' ) )
