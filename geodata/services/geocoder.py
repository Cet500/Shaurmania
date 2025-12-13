from datetime import date
import requests
from django.db import models as m, transaction

from Shaurmania.settings import GEO_CODER_KEY, GEO_CODER_LIMIT


class GeocodeStat( m.Model ):
	"""Счётчик запросов к геокодеру по дням."""
	date  = m.DateField( unique = True, db_index = True )
	count = m.PositiveIntegerField( default = 0 )

	def __str__(self):
		return f'Geocode by {self.date} - {self.count} requests'

	class Meta:
		verbose_name = 'Геокодер счётчик'
		verbose_name_plural = 'Геокодер счётчики'
		db_table = 'tech_geocode_stats'
		ordering = [ '-date' ]


YANDEX_GEOCODER_URL = 'https://geocode-maps.yandex.ru/v1/'


class Geocoder:
	"""
	Сервис геокодирования.
	Инициализируется строкой запроса (обычно full_address или его часть).
	"""
	def __init__( self, query: str ):
		self.query = query
		self._geo_object = None

	def can_call_api( self ) -> bool:
		"""Проверка, не превышен ли дневной лимит."""
		today = date.today()
		stat, _ = GeocodeStat.objects.get_or_create( date = today )

		return stat.count < GEO_CODER_LIMIT

	def get_geo_object(self) -> dict | None:
		"""
		Возвращает первый GeoObject (ленивый вызов).
		Если лимит превышен или ошибка — None.
		"""
		if self._geo_object is not None:
			return self._geo_object

		if not self.can_call_api():
			self._geo_object = None
			return None

		params = {
			'apikey'  : GEO_CODER_KEY,
			'geocode' : self.query,
			'format'  : 'json',
			'results' : 1,
			'lang'    : 'ru_RU',
		}

		try:
			resp = requests.get(YANDEX_GEOCODER_URL, params = params, timeout = 5)
			resp.raise_for_status()
			data = resp.json()

			collection = data.get('response', {}).get('GeoObjectCollection', {})
			members = collection.get('featureMember', [])

			if not members:
				geo = None
			else:
				geo = members[0].get('GeoObject')

		except Exception:
			geo = None

		# Увеличиваем счётчик только если реально ходили в API
		self._inc_counter()
		self._geo_object = geo

		return geo

	def get_formatted_address( self ) -> str | None:
		geo = self.get_geo_object()

		if not geo:
			return None

		meta = geo.get( 'metaDataProperty', { } ).get( 'GeocoderMetaData', { } )
		addr = meta.get( 'Address', { } )
		return addr.get( 'formatted' )

	def get_coordinates( self ) -> tuple[float, float] | None:
		geo = self.get_geo_object()

		if not geo:
			return None

		point = geo.get( 'Point', { } ) or { }
		pos = point.get( 'pos' )

		if not pos:
			return None

		try:
			lon_str, lat_str = pos.split()
			return float( lat_str ), float( lon_str )

		except (ValueError, TypeError):
			return None

	@classmethod
	@transaction.atomic
	def _inc_counter(cls):
		today = date.today()
		stat, _ = GeocodeStat.objects.select_for_update().get_or_create( date = today )

		if stat.count < GEO_CODER_LIMIT:
			stat.count += 1
			stat.save()
