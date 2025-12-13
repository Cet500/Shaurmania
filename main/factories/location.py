from factory import LazyAttribute
from factory.django import DjangoModelFactory, ImageField

from main.models import Location, TIME_VARIANTS

from .base import fake


class LocationFactory( DjangoModelFactory ):
	class Meta:
		model = Location

	name        = LazyAttribute( lambda _: fake.word() )
	description = LazyAttribute( lambda _: fake.text( max_nb_chars = 600 ) )
	planet      = LazyAttribute( lambda _: fake.word() )
	country     = LazyAttribute( lambda _: fake.country() )
	city        = LazyAttribute( lambda _: fake.city() )
	address     = LazyAttribute( lambda _: fake.address() )
	picture     = ImageField( width = 300, height = 300, color = 'white' )
	timeline    = LazyAttribute( lambda _: fake.random_element( elements = tuple( TIME_VARIANTS.keys() ) ) )
	contacts    = LazyAttribute( lambda _: fake.phone_number() )
	open_hours  = LazyAttribute( lambda _: fake.time() )
	close_hours = LazyAttribute( lambda _: fake.time() )
