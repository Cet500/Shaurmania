from django.db import models as m
from slugify import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class News( m.Model ):
	title        = m.CharField( max_length = 100, verbose_name = 'Заголовок' )
	slug         = m.SlugField( max_length = 110, blank = True, verbose_name = 'URL-адрес' )
	short_text   = m.TextField( max_length = 200, blank = True, verbose_name = 'Краткое описание' )
	main_text    = m.TextField( max_length = 1000, blank = True, verbose_name = 'Текст новости' )
	picture      = m.ImageField( upload_to = 'news_images', blank=True, null=True, verbose_name = 'Изображение 16 на 9' )
	thumbnail_bg = ImageSpecField(
		source = 'picture',
		processors = [ResizeToFill( 1600, 900 )],
		format = 'PNG',
		options = { 'quality': 90 },
	)
	thumbnail_md = ImageSpecField(
		source = 'picture',
		processors = [ResizeToFill( 800, 450 )],
		format = 'PNG',
		options = { 'quality': 90 },
	)
	thumbnail_sm = ImageSpecField(
		source = 'picture',
		processors = [ResizeToFill( 448, 252 )],
		format = 'PNG',
		options = { 'quality': 90 },
	)
	is_shown     = m.BooleanField( default = True, verbose_name = 'Доступна для показа' )
	is_important = m.BooleanField( default = False, verbose_name = 'Важная новость' )
	tags         = m.ManyToManyField( 'NewsTag', blank = True, verbose_name = 'Новостные теги' )
	created_at   = m.DateTimeField( auto_now_add = True, verbose_name = 'Дата создания' )
	updated_at   = m.DateTimeField( auto_now = True, verbose_name = 'Дата обновления' )

	def save( self, *args, **kwargs ):
		if not self.slug:
			self.slug = slugify( self.title )
		super().save( *args, **kwargs )

		if self.picture:
			self.thumbnail_bg.generate()
			self.thumbnail_md.generate()
			self.thumbnail_sm.generate()

	def __str__( self ):
		return f'{self.title}'

	class Meta:
		verbose_name = 'новость'
		verbose_name_plural = 'новости'
		ordering = ['-created_at', 'title']


class NewsTag( m.Model ):
	name       = m.CharField( max_length = 50, unique = True, verbose_name = 'Название тега' )
	slug       = m.SlugField( max_length = 60, blank = True, verbose_name = 'URL-адрес тега' )
	created_at = m.DateTimeField( auto_now_add = True, verbose_name = 'Дата создания' )

	def save( self, *args, **kwargs ):
		if not self.slug:
			self.slug = slugify( self.name )
		super().save( *args, **kwargs )

	def __str__( self ):
		return self.name

	class Meta:
		verbose_name = 'новостной тег'
		verbose_name_plural = 'новостные теги'
