from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory, ImageField

from main.models import Shaurma, ShaurmaCategory, ShaurmaImage

from .base import fake


class ShaurmaCategoryFactory( DjangoModelFactory ):
	class Meta:
		model = ShaurmaCategory

	name        = LazyAttribute( lambda _: fake.word() )
	description = LazyAttribute( lambda _: fake.text( max_nb_chars = 200 ) )
	order       = LazyAttribute( lambda _: fake.random_int( 0, 10 ) )


class ShaurmaFactory( DjangoModelFactory ):
	class Meta:
		model = Shaurma

	name        = LazyAttribute( lambda _: fake.word() )
	category    = SubFactory( ShaurmaCategoryFactory )
	compound    = LazyAttribute( lambda _: fake.text( max_nb_chars = 600 ) )
	short_text  = LazyAttribute( lambda _: fake.text( max_nb_chars = 200 ) )
	description = LazyAttribute( lambda _: fake.text( max_nb_chars = 1000 ) )
	picture     = ImageField( width = 300, height = 300, color = 'white' )
	price       = LazyAttribute( lambda _: fake.random_int( 100, 900 ) )
	weight      = LazyAttribute( lambda _: fake.random_int( 400, 600 ) )


class ShaurmaImageFactory( DjangoModelFactory ):
	class Meta:
		model = ShaurmaImage

	shaurma = SubFactory( ShaurmaFactory )
	image   = ImageField( width = 300, height = 300, color = 'white' )
	caption = LazyAttribute( lambda _: fake.sentence( nb_words = 3 ) )
	order   = LazyAttribute( lambda _: fake.random_int( 0, 10 ) )

