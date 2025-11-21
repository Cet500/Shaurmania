from django.db import models as m
from slugify import slugify


class News( m.Model ):
	title       = m.CharField( max_length = 100, verbose_name = 'Заголовок' )
	slug        = m.SlugField( max_length = 110, blank = True, verbose_name = "URL-адрес" )
	short_text  = m.TextField( max_length = 200, blank = True, verbose_name = 'Краткое описание' )
	description = m.TextField( max_length = 1000, blank = True, verbose_name = 'Описание' )
	picture     = m.ImageField( upload_to = 'news_images', verbose_name = 'Изображение' )
	is_shown    = m.BooleanField( default = True, verbose_name = "Доступна для показа" )
	created_at  = m.DateTimeField( auto_now_add = True, verbose_name = "Дата создания" )
	updated_at  = m.DateTimeField( auto_now = True, verbose_name = "Дата обновления" )

	def save( self, *args, **kwargs ):
		if not self.slug:
			self.slug = slugify( self.title )
		super().save( *args, **kwargs )

	def __str__( self ):
		return f'{self.title}'

	class Meta:
		verbose_name = 'новость'
		verbose_name_plural = 'новости'
		ordering = ['created_at', 'title']
