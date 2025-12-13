from factory import LazyAttribute, Sequence
from factory.django import DjangoModelFactory, ImageField

from main.models import News, NewsTag

from .base import fake


class NewsTagFactory( DjangoModelFactory ):
	class Meta:
		model = NewsTag

	name = Sequence( lambda n: f'Тег {n}' )


class NewsFactory( DjangoModelFactory ):
	class Meta:
		model = News

	title        = Sequence( lambda n: f'Новость {n}' )
	short_text   = LazyAttribute( lambda _: fake.text( max_nb_chars = 180 ) )
	rich_content = LazyAttribute( lambda _: fake.text( max_nb_chars = 1000 ) )
	picture      = ImageField( width = 800, height = 450, color = 'white' )
	is_shown     = LazyAttribute( lambda _: fake.boolean() )
	is_important = LazyAttribute( lambda _: fake.boolean() )

	@classmethod
	def _create( cls, model_class, *args, **kwargs ):
		tags = kwargs.pop(
			'tags', [NewsTagFactory() for _ in range( fake.random_int( 1, 3 ) )]
		)
		news = super()._create( model_class, *args, **kwargs )

		if tags:
			news.tags.set( tags )

		return news

