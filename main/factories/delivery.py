from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from main.models.delivery import Delivery, SPEED_TYPES

from .base import fake
from geodata.factories import GeoCityFactory


class DeliveryFactory(DjangoModelFactory):
	class Meta:
		model = Delivery

	city = SubFactory(GeoCityFactory)
	delivery_price = LazyAttribute(lambda _: fake.random_int(100, 500))
	delivery_speed = LazyAttribute(lambda _: fake.random_element(elements=tuple(SPEED_TYPES.keys())))

