from django.db import models as m


class TimeZone( m.Model ):
	tz = m.CharField(
		max_length = 64,
		unique = True,
		verbose_name = 'Таймзона (IANA)'
	)
	shift = m.IntegerField(
		verbose_name = 'Смещение UTC (часы)'
	)

	@property
	def by_utc( self ):
		return f'UTC{'+' if self.shift >= 0 else ''}{self.shift}'

	def __str__( self ):
		return f"{self.tz} (UTC{'+' if self.shift >= 0 else ''}{self.shift})"

	class Meta:
		verbose_name = 'таймзона'
		verbose_name_plural = 'таймзоны'
		db_table = 'geo_timezones'
		ordering = ['tz']
