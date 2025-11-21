from django.test import TestCase
from django.conf import settings


class SettingsSanityTestCase( TestCase ):
	def test_required_settings_exist( self ):
		"""Проверяем, что все обязательные настройки существуют"""
		required_settings = [
			'BASE_DIR',
			'SECRET_KEY',
			'DEBUG',
			'ALLOWED_HOSTS',
			'DATABASES',
			'INSTALLED_APPS',
			'MIDDLEWARE',
			'TEMPLATES',
			'LOGGING'
		]

		missing_settings = []

		for setting in required_settings:
			if not hasattr( settings, setting ):
				missing_settings.append( setting )

		self.assertEqual(
			len( missing_settings ),
			0,
			f"Отсутствуют обязательные настройки: {missing_settings}"
		)
