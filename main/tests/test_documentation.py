import os
from django.test import TestCase
from Shaurmania.settings import BASE_DIR


class DocumentationTestCase( TestCase ):
	def test_required_docs_exist( self ):
		"""Проверяем, что есть необходимая документация"""
		required_files = [
			'LICENSE',
			'README.md',
			'requirements.txt',
			'.env.example',
		]

		missing_files = []

		for file in required_files:
			if not os.path.exists( os.path.join( BASE_DIR, file ) ):
				missing_files.append( file )

		self.assertEqual(
			len( missing_files ),
			0,
			f"Отсутствуют необходимые файлы: {missing_files}"
		)
