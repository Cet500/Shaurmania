from django.db import models as m
from slugify import slugify


TIME_VARIANTS = {
	'PST': 'Прошлое',
	'NOW': 'Настоящее',
	'FTR': 'Будущее'
}

class Location( m.Model ):
	name        = m.CharField( max_length = 60, verbose_name = 'Название' )
	slug        = m.SlugField( max_length = 70, blank = True, verbose_name = "URL-адрес" )
	description = m.TextField( max_length = 600, verbose_name = 'Описание' )
	planet      = m.CharField( max_length = 60, default = 'Земля', verbose_name = 'Планета' )
	country     = m.CharField( max_length = 60, default = 'Россия', verbose_name = 'Страна' )
	city        = m.CharField( max_length = 30, verbose_name = 'Город' )
	address     = m.CharField( max_length = 60, verbose_name = 'Адрес' )
	picture     = m.ImageField( upload_to = 'locations', verbose_name = 'Изображение' )
	timeline    = m.CharField( max_length = 3, default = 'NOW', choices = TIME_VARIANTS, verbose_name = 'Время' )
	contacts    = m.CharField( max_length = 60, verbose_name = 'Контакты' )
	open_hours  = m.TimeField( verbose_name = 'Начало' )
	close_hours = m.TimeField( verbose_name = 'Конец' )
	created_at  = m.DateTimeField( auto_now_add = True, verbose_name = 'Дата добавления' )
	updated_at  = m.DateTimeField( auto_now = True, verbose_name = "Дата обновления" )

	def save( self, *args, **kwargs ):
		if not self.slug:
			self.slug = slugify( self.name )
		super().save( *args, **kwargs )

	def __str__( self ):
		return f'{self.name}'

	class Meta:
		verbose_name = 'заведениe'
		verbose_name_plural = 'заведения'
		ordering = ['address']
