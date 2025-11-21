from django.apps import apps
from django.test import TestCase


class ModelsStrTestCase( TestCase ):
	def test_all_models_have_str_method( self ):
		"""Проверяем, что все модели имеют __str__ метод"""
		models = apps.get_models()
		models_without_str = []

		for model in models:
			# Пропускаем модели из сторонних приложений
			if not model.__module__.startswith( 'your_project_name' ):
				continue

			if '__str__' not in model.__dict__:
				models_without_str.append( f"{model.__module__}.{model.__name__}" )

		self.assertEqual(
			len( models_without_str ),
			0,
			f"Модели без __str__ метода: {models_without_str}"
		)