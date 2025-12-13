import json
from typing import Any, Dict, Optional

import maxminddb

from datetime import datetime, timezone

from ipaddress import ip_address
from geodata.models import GeoCountry
from Shaurmania.settings import GEOIP_DATABASE


def get_country_by_ip( ip: str ) -> GeoCountry | None:
	try:
		ip_obj = ip_address( ip )
	except ValueError:
		return None

	country = None

	with maxminddb.open_database(GEOIP_DATABASE) as reader:
		data = reader.get( ip )
		country = GeoCountry.objects.filter( cca2 = data['country_code'] ).first()

	return country


DATETIME_FORMATS = [
	"%Y-%m-%d %H:%M:%S",
	"%Y-%m-%d %H:%M:%S.%f",
	"%Y-%m-%dT%H:%M:%S",
	"%Y-%m-%d",
]


def parse_dt( value: Any ) -> Optional[datetime]:
	"""Парсит datetime и приводит к UTC aware"""
	if not value:
		return None

	if isinstance( value, datetime ):
		if value.tzinfo is None:
			return value.replace( tzinfo = timezone.utc )
		return value.astimezone( timezone.utc )

	s = str( value ).strip()

	for fmt in DATETIME_FORMATS:
		try:
			dt = datetime.strptime( s, fmt )
			return dt.replace( tzinfo = timezone.utc )
		except ValueError:
			continue

	raise ValueError( f"Unknown datetime format: {value}" )


def to_float(value: Any) -> Optional[float]:
	"""Преобразует в float или None"""
	if value in (None, ""):
		return None
	try:
		return float(value)
	except (TypeError, ValueError):
		return None


def to_int(value: Any) -> Optional[int]:
	"""Преобразует в int или None"""
	if value in (None, ""):
		return None
	try:
		return int(value)
	except (TypeError, ValueError):
		return None


def parse_translations(translations_raw: str, default_lang: str = "en") -> Dict[str, str]:
	"""Парсит JSON translations. Возвращает dict с ключами языков."""
	if not translations_raw:
		return {}
	try:
		return json.loads(translations_raw)
	except json.JSONDecodeError:
		return {}


def get_localized_name(translations: Dict[str, str], original_name: str, lang: str = "ru") -> str:
	"""Извлекает локализованное имя или возвращает оригинальное"""
	return translations.get(lang) or original_name


class SimpleCache:
	"""Кеш с автозагрузкой из БД по функции"""

	def __init__( self, loader_func ):
		self._cache = { }
		self._loader = loader_func

	def get( self, key: str ) -> Any:
		if key not in self._cache:
			self._cache[key] = self._loader( key )
		return self._cache[key]

	def set( self, key: str, value: Any ):
		self._cache[key] = value

	def clear( self ):
		self._cache.clear()
