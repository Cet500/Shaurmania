import mimetypes
import os

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from Shaurmania.settings import (
	FORBIDDEN_FILE_EXTENSIONS,
	ALLOWED_MIME_TYPES,
	MAX_FILES_SIZES
)


@deconstructible
class FileValidator:
	"""Валидатор файлов для чата"""
	def __call__( self, value ):
		# Проверка расширения
		ext = os.path.splitext( value.name )[1].lower()
		if ext in FORBIDDEN_FILE_EXTENSIONS:
			raise ValidationError( f'Файлы с расширением {ext} запрещены для загрузки' )

		# Проверка MIME типа по расширению
		mime_type, _ = mimetypes.guess_type( value.name )
		if not mime_type:
			raise ValidationError( 'Не удалось определить тип файла' )

		# Определяем категорию по MIME типу для дальнейшей проверки размера
		category = self._get_category_by_mime( mime_type )

		# Проверка двойного расширения
		if self._has_double_extension( value.name ):
			raise ValidationError( 'Файл с двойным расширением не разрешен' )

		# Проверка размера файла
		if hasattr( value, 'size' ):
			file_size = value.size

			max_size = MAX_FILES_SIZES.get( category, MAX_FILES_SIZES['other'] )

			if file_size > max_size:
				size_mb = max_size // 1024 // 1024
				raise ValidationError(
					f'Максимальный размер файла для типа {category}: {size_mb} МБ'
				)

			if file_size == 0:
				raise ValidationError( 'Файл не может быть пустым' )

	def _get_category_by_mime( self, mime_type ):
		"""Определяет категорию файла по MIME типу"""
		for category, mimes in ALLOWED_MIME_TYPES.items():
			if mime_type in mimes:
				return category

		return 'other'

	def _has_double_extension( self, filename ):
		"""Проверяет наличие двойного расширения (например, file.exe.jpg)"""
		name = filename.lower()
		parts = name.split( '.' )

		# Если есть более двух частей (имя.расширение1.расширение2), это двойное расширение
		if len( parts ) > 2:
			last_ext = '.' + parts[-1]
			second_last_ext = '.' + parts[-2]

			# Проверяем, если хотя бы одно из расширений запрещено
			if last_ext in FORBIDDEN_FILE_EXTENSIONS or second_last_ext in FORBIDDEN_FILE_EXTENSIONS:
				return True

		return False