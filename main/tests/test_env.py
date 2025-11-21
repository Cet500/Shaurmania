import os
from django.test import TestCase
from Shaurmania.settings import BASE_DIR


class EnvFilesTestCase( TestCase ):
	def test_env_keys_match_example( self ):
		"""Проверяет, что все ключи из .env.example присутствуют в .env"""

		# Получаем пути к файлам
		example_path = os.path.join( BASE_DIR, '.env.example' )
		env_path = os.path.join( BASE_DIR, '.env' )

		# Проверяем существование файлов
		self.assertTrue( os.path.exists( example_path ),
		                 ".env.example не найден в корне проекта" )
		self.assertTrue( os.path.exists( env_path ),
		                 ".env не найден в корне проекта" )

		# Читаем ключи из файлов
		example_keys = self._parse_env_keys( example_path )
		env_keys = self._parse_env_keys( env_path )

		# Проверяем отсутствующие ключи
		missing_keys = example_keys - env_keys
		self.assertEqual(
			len( missing_keys ),
			0,
			f"В .env отсутствуют ключи: {missing_keys}"
		)

	def _parse_env_keys( self, file_path ):
		"""Парсит ключи из env-файла"""
		keys = set()
		with open( file_path, 'r' ) as f:
			for line in f:
				line = line.strip()
				# Пропускаем пустые строки и комментарии
				if not line or line.startswith( '#' ) or '=' not in line:
					continue

				# Извлекаем ключ (часть до первого =)
				key = line.split( '=', 1 )[0].strip()
				# Убираем префикс export (для bash-экспорта)
				if key.startswith( 'export ' ):
					key = key[7:].strip()
				keys.add( key )
		return keys
