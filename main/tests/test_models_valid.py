from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase


class ModelsValidationTestCase( TestCase ):
	def test_all_models_can_validate( self ):
		"""Проверяем, что все модели могут пройти базовую валидацию"""
		models = apps.get_models()
		invalid_models = []

		for model in models:
			try:
				# Пробуем создать экземпляр с минимальными данными
				instance = model()
				instance.clean()  # Вызываем валидацию
			except (ValidationError, Exception) as e:
				invalid_models.append( f"{model.__name__}: {str( e )}" )

		self.assertEqual(
			len( invalid_models ),
			0,
			f"Проблемы с валидацией моделей:\n" + "\n".join( invalid_models )
		)
