from django.test import TestCase
from django.conf import settings


class InstalledAppsTestCase( TestCase ):
	def test_no_duplicate_installed_apps( self ):
		"""Проверяем, что нет дубликатов в INSTALLED_APPS"""
		installed_apps = settings.INSTALLED_APPS

		seen = set()
		duplicates = set()

		for app in installed_apps:
			if app in seen:
				duplicates.add( app )
			seen.add( app )

		self.assertEqual(
			len( duplicates ),
			0,
			f"Найдены дубликаты в INSTALLED_APPS: {duplicates}"
		)
