from django.db import models as m
from slugify import slugify


class Stock( m.Model ):
	slug = m.SlugField( max_length = 70, blank = True, verbose_name = "URL-адрес" )
	name = m.CharField( max_length = 60, verbose_name = 'Название' )
	short_text = m.CharField( max_length = 150, blank = True, verbose_name = 'Краткое описание' )
	description = m.TextField( max_length = 1000, blank = True, verbose_name = 'Описание' )
	condition = m.TextField( max_length = 1000, blank = True, verbose_name = 'Условия акции' )
	image = m.ImageField( upload_to = 'stocks', verbose_name = 'Изображение' )
	discount = m.SmallIntegerField( verbose_name = 'Скидка в %' )
	categories = m.ManyToManyField( 'ShaurmaCategory', blank = True, verbose_name = 'Категория' )
	date_start = m.DateField( verbose_name = 'Старт' )
	date_end = m.DateField( verbose_name = 'Завершение' )

	def save( self, *args, **kwargs ):
		if not self.slug:
			self.slug = slugify( self.name )
		super().save( *args, **kwargs )

	def __str__( self ):
		return f'{self.name}'


	class Meta:
		verbose_name = 'акция'
		verbose_name_plural = 'акции'
		ordering = ['name']
