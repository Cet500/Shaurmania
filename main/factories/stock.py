from factory import LazyAttribute
from factory.django import DjangoModelFactory, ImageField

from main.models import Stock

from .base import fake
from .shaurma import ShaurmaCategoryFactory


class StockFactory( DjangoModelFactory ):
	class Meta:
		model = Stock

	name        = LazyAttribute( lambda _: fake.word() )
	short_text  = LazyAttribute( lambda _: fake.text( max_nb_chars = 160 ) )
	description = LazyAttribute( lambda _: fake.text( max_nb_chars = 1000 ) )
	condition   = LazyAttribute( lambda _: fake.text( max_nb_chars = 1000 ) )
	image       = ImageField( width = 300, height = 300, color = 'white' )
	discount    = LazyAttribute( lambda _: fake.random_int( 5, 95 ) )
	date_start  = LazyAttribute( lambda _: fake.date_between( start_date = '-30d', end_date = 'today' ) )
	date_end    = LazyAttribute( lambda o: fake.date_between( start_date = o.date_start, end_date = '+30d' ) )

	@classmethod
	def _create( cls, model_class, *args, **kwargs ):
		categories = kwargs.pop(
			'categories', [ShaurmaCategoryFactory() for _ in range( fake.random_int( 1, 3 ) )]
		)
		stock = super()._create( model_class, *args, **kwargs )

		if categories:
			stock.categories.set( categories )

		return stock

