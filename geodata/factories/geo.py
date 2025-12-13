import itertools

from factory import LazyAttribute, Sequence, SubFactory
from factory.django import DjangoModelFactory

from geodata.models import (
	GeoPartWorld, GeoRegionWorld, GeoCountry,
	GeoNodeType, GeoNode, GeoCity,
	GeoStreetType, GeoStreet
)

from .base import fake
from .timezones import TimeZoneFactory


class GeoPartWorldFactory(DjangoModelFactory):
	class Meta:
		model = GeoPartWorld

	name_ru = LazyAttribute(lambda obj: fake.word())
	name_en = LazyAttribute(lambda obj: fake.word())
	wiki_data_id = Sequence(lambda n: f'Q{n}')


class GeoRegionWorldFactory(DjangoModelFactory):
	class Meta:
		model = GeoRegionWorld

	part_world = SubFactory(GeoPartWorldFactory)
	name_ru = LazyAttribute(lambda _: fake.word())
	name_en = LazyAttribute(lambda _: fake.word())
	wiki_data_id = Sequence(lambda n: f'Q{n}')


class GeoCountryFactory(DjangoModelFactory):
	class Meta:
		model = GeoCountry

	region_world = SubFactory(GeoRegionWorldFactory)
	name_ru = LazyAttribute(lambda _: fake.country())
	name_official_ru = LazyAttribute(lambda o: f'Официальное название {o.name_ru}')
	name_en = LazyAttribute(lambda _: fake.country())
	name_official_en = LazyAttribute(lambda o: f'Official name of {o.name_en}')
	capital_ru = LazyAttribute(lambda _: fake.city())
	capital_en = LazyAttribute(lambda _: fake.city())
	emoji_code = LazyAttribute(lambda _: fake.pystr(min_chars=2, max_chars=2).upper())
	emoji_flag = LazyAttribute(lambda _: fake.pystr(min_chars=1, max_chars=1))
	currency_code = LazyAttribute(lambda _: fake.random_element(elements=('RUB', 'USD', 'EUR', 'GBP', 'JPY', 'CNY')))
	currency_name = LazyAttribute(lambda _: fake.random_element(elements=('Рубль', 'Доллар', 'Евро', 'Фунт', 'Йена', 'Юань')))
	currency_symbol = LazyAttribute(lambda _: fake.random_element(elements=('₽', '$', '€', '£', '¥', '元')))
	phone_code = LazyAttribute(lambda _: f'+{fake.random_int(1, 999)}')
	cca2 = LazyAttribute(lambda _: fake.pystr(min_chars=2, max_chars=2).upper())
	cca3 = LazyAttribute(lambda _: fake.pystr(min_chars=3, max_chars=3).upper())
	ccn3 = LazyAttribute(lambda _: f'{fake.random_int(100, 999):03d}')
	top_level_domain = LazyAttribute(lambda _: f'.{fake.pystr(min_chars=2, max_chars=3).lower()}')
	is_landlocked = LazyAttribute(lambda _: fake.boolean())
	is_independent = LazyAttribute(lambda _: fake.boolean())
	is_member_oon = LazyAttribute(lambda _: fake.boolean())
	area = LazyAttribute(lambda _: fake.random_int(1000, 20_000_000))
	population = LazyAttribute(lambda _: fake.random_int(100_000, 1_500_000_000))
	latitude = LazyAttribute(lambda _: fake.latitude())
	longitude = LazyAttribute(lambda _: fake.longitude())
	wiki_data_id = Sequence(lambda n: f'Q{n}')
	is_handly_verify = LazyAttribute(lambda _: fake.boolean())


class GeoNodeTypeFactory(DjangoModelFactory):
	class Meta:
		model = GeoNodeType

	name_en = LazyAttribute(lambda _: fake.word())
	name_ru = LazyAttribute(lambda _: fake.word())
	description_en = LazyAttribute(lambda _: fake.text(max_nb_chars=250))
	description_ru = LazyAttribute(lambda _: fake.text(max_nb_chars=250))


class GeoNodeFactory(DjangoModelFactory):
	class Meta:
		model = GeoNode

	country = SubFactory(GeoCountryFactory)
	node_type = SubFactory(GeoNodeTypeFactory)
	parent = None
	level = LazyAttribute(lambda _: fake.random_int(1, 5))
	name_ru = LazyAttribute(lambda _: fake.random_element(elements=('Московская область', 'Ленинградская область', 'Краснодарский край', 'Республика Татарстан')))
	name_en = LazyAttribute(lambda _: fake.random_element(elements=('Moscow Oblast', 'Leningrad Oblast', 'Krasnodar Krai', 'Republic of Tatarstan')))
	name_native = LazyAttribute(lambda o: o.name_ru)
	latitude = LazyAttribute(lambda _: fake.latitude())
	longitude = LazyAttribute(lambda _: fake.longitude())
	timezone = SubFactory(TimeZoneFactory)
	population = LazyAttribute(lambda _: fake.random_int(10000, 50_000_000) if fake.boolean() else None)
	iso_code = LazyAttribute(lambda _: f'{fake.pystr(min_chars=2, max_chars=2).upper()}-{fake.pystr(min_chars=2, max_chars=3).upper()}' if fake.boolean() else None)
	wiki_data_id = LazyAttribute(lambda _: f'Q{fake.random_int(100, 999)}' if fake.boolean() else None)
	created_at = LazyAttribute(lambda _: fake.date_time_between(start_date='-1y', end_date='now'))
	updated_at = LazyAttribute(lambda _: fake.date_time_between(start_date='-1y', end_date='now'))


class GeoCityFactory(DjangoModelFactory):
	class Meta:
		model = GeoCity

	node = SubFactory(GeoNodeFactory)
	name_ru = LazyAttribute(lambda _: fake.city())
	name_en = LazyAttribute(lambda _: fake.city())
	name_native = LazyAttribute(lambda o: o.name_ru)
	latitude = LazyAttribute(lambda _: fake.latitude())
	longitude = LazyAttribute(lambda _: fake.longitude())
	timezone = SubFactory(TimeZoneFactory)
	population = LazyAttribute(lambda _: fake.random_int(1000, 20_000_000) if fake.boolean() else None)
	wiki_data_id = LazyAttribute(lambda _: f'Q{fake.random_int(100, 999)}' if fake.boolean() else None)
	created_at = LazyAttribute(lambda _: fake.date_time_between(start_date='-1y', end_date='now'))
	updated_at = LazyAttribute(lambda _: fake.date_time_between(start_date='-1y', end_date='now'))


class GeoStreetTypeFactory(DjangoModelFactory):
	class Meta:
		model = GeoStreetType

	id = Sequence( lambda n: n + 1 )  # Явно задаём ID

	short_ru = LazyAttribute( lambda obj: fake.word() )
	long_ru  = LazyAttribute( lambda obj: fake.pystr(min_chars=2, max_chars=5) )
	short_en = LazyAttribute( lambda obj: fake.word() )
	long_en  = LazyAttribute( lambda obj: fake.pystr(min_chars=2, max_chars=5) )
	variants_ru = LazyAttribute( lambda obj: [obj.short_ru, obj.long_ru] )
	variants_en = LazyAttribute( lambda obj: [obj.short_en, obj.long_en] )
	order = LazyAttribute( lambda obj: obj.id )


class GeoStreetFactory(DjangoModelFactory):
	class Meta:
		model = GeoStreet

	city = SubFactory(GeoCityFactory)
	street_type = SubFactory(GeoStreetTypeFactory)
	name_native = LazyAttribute(lambda _: fake.random_element(elements=('Ленина', 'Пушкина', 'Гагарина', 'Мира', 'Советская', 'Центральная', 'Октябрьская')))

