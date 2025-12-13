import json
from datetime import datetime, timezone

from geodata.models import GeoCity, GeoNode, TimeZone
from geodata.utils import parse_dt, to_float, to_int, parse_translations, get_localized_name, SimpleCache
from .base_geo_import import BaseGeoImportCommand


class Command( BaseGeoImportCommand ):
	help = "Импорт/обновление городов из temp/cities.sqlite3"

	SOURCE_DB_NAME = "cities.sqlite3"
	TABLE_NAME     = "cities"
	LOG_INTERVAL    = 500

	def __init__( self, *args, **kwargs ):
		super().__init__( *args, **kwargs )
		self.node_cache = SimpleCache( self._load_node )
		self.tz_cache = SimpleCache( self._load_tz )

	def _load_node( self, iso_code: str ) -> GeoNode:
		"""Загружает GeoNode по iso_code вида RU-PRI"""
		node = GeoNode.objects.filter( iso_code = iso_code ).first()
		if not node:
			# Fallback: по стране
			country_code = iso_code.split( "-" )[0] if "-" in iso_code else iso_code
			node = GeoNode.objects.filter( country__cca2 = country_code ).first()
		if not node:
			raise ValueError( f"GeoNode не найден для {iso_code}" )
		return node

	def _load_tz( self, tz_name: str ) -> TimeZone:
		"""Загружает TimeZone, при ошибке возвращает None"""
		try:
			return TimeZone.objects.get( tz = tz_name )
		except TimeZone.DoesNotExist:
			return None

	def _process_row( self, row ):
		"""Обработка строки cities"""
		country_code = row["country_code"]
		state_code = row["state_code"]
		city_name = row["name"]
		tz_name = row["timezone"]

		# Находим регион по RU-PRI
		node_iso_code = f"{country_code}-{state_code}"
		district = self.node_cache.get( node_iso_code )

		# Timezone
		tz_obj = self.tz_cache.get( tz_name )

		# Парсим данные
		translations = parse_translations( row["translations"] )
		name_ru = get_localized_name( translations, city_name, "ru" )
		name_en = city_name
		name_native = row["native"] or city_name

		latitude = float( row["latitude"] )
		longitude = float( row["longitude"] )
		population = to_int( row["population"] )
		wiki_id = row["wikiDataId"]

		created_at_src = parse_dt( row["created_at"] )
		updated_at_src = parse_dt( row["updated_at"] )

		now_utc = datetime.now( timezone.utc )
		if not created_at_src:
			created_at_src = now_utc
		if not updated_at_src:
			updated_at_src = now_utc

		# Поиск GeoCity
		city = GeoCity.objects.filter( node = district, name_ru = name_ru ).first()

		if city is None:
			# Создаём
			city = GeoCity(
				node = district,
				name_ru = name_ru,
				name_en = name_en,
				name_native = name_native,
				latitude = latitude,
				longitude = longitude,
				timezone = tz_obj,
				population = population,
				wiki_data_id = wiki_id or None,
				created_at = created_at_src,
				updated_at = updated_at_src,
			)
			city.save()
			self.created += 1
		else:
			# Обновляем по дате
			if self._should_update( city, updated_at_src ):
				city.node = district
				city.name_ru = name_ru
				city.name_en = name_en
				city.name_native = name_native
				city.latitude = latitude
				city.longitude = longitude
				city.timezone = tz_obj
				city.population = population
				city.wiki_data_id = wiki_id or None
				city.created_at = created_at_src
				city.updated_at = updated_at_src
				city.save()
				self.updated += 1
			else:
				self.skipped += 1
