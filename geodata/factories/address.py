from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from geodata.models.address import BaseAddress, Address

from .base import fake
from .geo import GeoStreetFactory


class BaseAddressFactory(DjangoModelFactory):
	class Meta:
		model = BaseAddress

	street      = SubFactory( GeoStreetFactory )
	house       = LazyAttribute( lambda _: f'{fake.random_int(1, 250)}' )
	building    = LazyAttribute( lambda _: fake.pystr(min_chars=1, max_chars=3).upper() if fake.boolean() else '' )
	postal_code = LazyAttribute( lambda _: f'{fake.random_int(100000, 999999)}' if fake.boolean() else None )
	latitude    = LazyAttribute( lambda _: fake.latitude() )
	longitude   = LazyAttribute( lambda _: fake.longitude() )
	is_verified = LazyAttribute( lambda _: True )


class AddressFactory(DjangoModelFactory):
	class Meta:
		model = Address

	base      = SubFactory( BaseAddressFactory )
	entrance  = LazyAttribute( lambda _: fake.random_int(1, 40) )
	floor     = LazyAttribute( lambda _: fake.random_int(1, 250) )
	apartment = LazyAttribute( lambda _: fake.random_int(1, 30000) )
	intercom  = LazyAttribute( lambda _: fake.random_int(1000, 30000) )
	is_active = LazyAttribute( lambda _: fake.boolean() )
