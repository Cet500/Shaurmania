import os
import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class BaseGeoImportCommand( BaseCommand, ABC ):
	"""Базовый класс для импорта гео-данных из SQLite"""

	# Переопределить в подклассах
	SOURCE_DB_NAME = ""  # Имя файла (states.sqlite3, cities.sqlite3)
	TABLE_NAME     = ""  # Таблица в БД
	LOG_INTERVAL   = 1   # Логировать каждые N строк

	def __init__( self, *args, **kwargs ):
		super().__init__( *args, **kwargs )
		self.created = 0
		self.updated = 0
		self.skipped = 0
		self.errors = 0
		self.processed = 0
		self.total = 0

	def add_arguments( self, parser ):
		parser.add_argument(
			'--verbose',
			action = 'store_true',
			help = 'Выводить лог для каждой строки (медленно)',
		)

	def handle( self, *args, **options ):
		self.verbose = options.get( 'verbose', False )

		db_path = os.path.join( os.getcwd(), "temp", self.SOURCE_DB_NAME )
		if not os.path.exists( db_path ):
			raise CommandError( f"SQLite база не найдена: {db_path}" )

		self.stdout.write( f"Чтение SQLite: {db_path}" )

		conn = sqlite3.connect( db_path )
		conn.row_factory = sqlite3.Row

		try:
			rows = conn.execute( f"SELECT * FROM {self.TABLE_NAME}" ).fetchall()
		finally:
			conn.close()

		self.total = len( rows )
		self.stdout.write( f"Найдено записей в {self.TABLE_NAME}: {self.total}" )

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

		self._log_summary()

	def _log_progress( self ):
		"""Логировать прогресс по интервалу"""
		if self.processed % self.LOG_INTERVAL == 0:
			self.stdout.write(
				f"Обработано: {self.processed}/{self.total} "
				f"(✓{self.created} ↺{self.updated} ○{self.skipped})"
			)

	def _log_summary( self ):
		"""Логировать финальный результат"""
		self.stdout.write( self.style.SUCCESS(
			f"✓ Готово! created={self.created}, updated={self.updated}, "
			f"skipped={self.skipped}, errors={self.errors}"
		) )

	def _should_update( self, existing_obj, updated_at_src: datetime ) -> bool:
		"""Проверить, нужно ли обновлять объект"""
		if not hasattr( existing_obj, 'updated_at' ):
			return True
		if not updated_at_src:
			return True
		return updated_at_src > existing_obj.updated_at

	@abstractmethod
	def _process_row( self, row: sqlite3.Row ):
		"""Переопределить в подклассе для обработки каждой строки"""
		pass
