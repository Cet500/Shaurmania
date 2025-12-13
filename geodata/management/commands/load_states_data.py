import os
import sqlite3
from datetime import datetime, timezone

from django.core.management.base import CommandError
from django.db import transaction

from geodata.models import GeoNode, GeoCountry, GeoNodeType, TimeZone
from geodata.utils import parse_dt, to_float, to_int, parse_translations, get_localized_name, SimpleCache
from .base_geo_import import BaseGeoImportCommand


class Command( BaseGeoImportCommand ):
	help = "Импорт/обновление гео-узлов из temp/states.sqlite3"

	SOURCE_DB_NAME = "states.sqlite3"
	TABLE_NAME     = "states"
	LOG_INTERVAL   = 100

	def __init__( self, *args, **kwargs ):
		super().__init__( *args, **kwargs )
		self.country_cache = SimpleCache( lambda cc: GeoCountry.objects.get( cca2 = cc ) )
		self.tz_cache = SimpleCache( lambda tz: TimeZone.objects.get( tz = tz ) )
		self.id_map = { }  # old_id -> GeoNode.pk

	def handle( self, *args, **options ):
		# Читаем все строки
		db_path = os.path.join( os.getcwd(), "temp", self.SOURCE_DB_NAME )
		if not os.path.exists( db_path ):
			raise CommandError( f"SQLite база не найдена: {db_path}" )

		conn = sqlite3.connect( db_path )
		conn.row_factory = sqlite3.Row

		try:
			rows = conn.execute( f"SELECT * FROM {self.TABLE_NAME}" ).fetchall()
		finally:
			conn.close()

		self.total = len( rows )
		self.stdout.write( f"Найдено записей: {self.total}" )

		# 1-й проход: создаём/обновляем без parent
		self.stdout.write( "Первый проход: создание узлов..." )
		with transaction.atomic():
			for row in rows:
				try:
					self.processed += 1
					self._process_row( row )
					self._log_progress()
				except Exception as e:
					self.errors += 1
					self.stderr.write( f"[error] row id={row['id']}: {e}" )
					raise

		# 2-й проход: проставляем parent
		self.stdout.write( "Второй проход: установка parent-ссылок..." )
		self.processed = 0
		with transaction.atomic():
			for row in rows:
				try:
					old_id = row["id"]
					parent_id = row["parent_id"]

					if not parent_id:
						continue

					self.processed += 1
					node_pk = self.id_map.get( old_id )
					parent_pk = self.id_map.get( parent_id )

					if not node_pk or not parent_pk:
						raise CommandError(
							f"Не найдены связи для parent: old_id={old_id}, parent_id={parent_id}"
						)

					node = GeoNode.objects.get( pk = node_pk )
					parent = GeoNode.objects.get( pk = parent_pk )

					if node.parent_id != parent.pk:
						node.parent = parent
						node.save( update_fields = ["parent"] )

					if self.processed % 1000 == 0:
						self.stdout.write( f"Parent-ссылки: {self.processed}" )

				except Exception as e:
					self.errors += 1
					self.stderr.write( f"[error parent] row id={row['id']}: {e}" )
					raise

		self._log_summary()

	def _process_row( self, row ):
		"""Обработка строки states"""
		country_code = row["country_code"]
		state_name = row["name"]
		state_type = row["type"]
		tz_name = row["timezone"]

		# Получаем объекты с кешем
		country = self.country_cache.get( country_code )
		tz_obj = self.tz_cache.get( tz_name )

		# node_type
		node_type = None
		if state_type:
			node_type = GeoNodeType.objects.filter( name_en = state_type ).first()
		if not node_type:
			node_type = GeoNodeType.objects.get( pk = 0 )

		# Парсим данные
		translations = parse_translations( row["translations"] )
		name_ru = get_localized_name( translations, state_name, "ru" )
		name_en = state_name
		name_native = row["native"] or state_name

		latitude = to_float( row["latitude"] )
		longitude = to_float( row["longitude"] )
		population = to_int( row["population"] )
		iso_code = row["iso3166_2"] or None
		wiki_id = row["wikiDataId"]

		created_at_src = parse_dt( row["created_at"] )
		updated_at_src = parse_dt( row["updated_at"] )

		now_utc = datetime.now( timezone.utc )
		if not created_at_src:
			created_at_src = now_utc
		if not updated_at_src:
			updated_at_src = now_utc

		# Поиск GeoNode
		lookup = { "country": country }
		if iso_code:
			lookup["iso_code"] = iso_code
			node = GeoNode.objects.filter( **lookup ).first()
			if not node:
				lookup = { "country": country, "name_en": name_en }
				node = GeoNode.objects.filter( **lookup ).first()
		else:
			lookup = { "country": country, "name_en": name_en }
			node = GeoNode.objects.filter( **lookup ).first()

		if node is None:
			# Создаём
			node = GeoNode(
				country = country,
				node_type = node_type,
				parent = None,
				level = row["level"],
				name_ru = name_ru,
				name_en = name_en,
				name_native = name_native,
				latitude = latitude,
				longitude = longitude,
				timezone = tz_obj,
				population = population,
				iso_code = iso_code,
				wiki_data_id = wiki_id or None,
				created_at = created_at_src,
				updated_at = updated_at_src,
			)
			node.save()
			self.created += 1
		else:
			# Обновляем по дате
			if self._should_update( node, updated_at_src ):
				node.country = country
				node.node_type = node_type
				node.level = row["level"]
				node.name_ru = name_ru
				node.name_en = name_en
				node.name_native = name_native
				node.latitude = latitude
				node.longitude = longitude
				node.timezone = tz_obj
				node.population = population
				node.iso_code = iso_code
				node.wiki_data_id = wiki_id or None
				node.created_at = created_at_src
				node.updated_at = updated_at_src
				node.save()
				self.updated += 1
			else:
				self.skipped += 1

		self.id_map[row["id"]] = node.pk
