from django.core.exceptions import ValidationError
from django.test import TestCase

from geodata.factories import (
	TimeZoneFactory,
	GeoPartWorldFactory,
	GeoRegionWorldFactory,
	GeoCountryFactory,
	GeoNodeTypeFactory,
	GeoNodeFactory,
	GeoCityFactory,
	GeoStreetTypeFactory,
	GeoStreetFactory,
	BaseAddressFactory,
	AddressFactory,
)
from geodata.models.geo import (
	GeoPartWorld, GeoRegionWorld, GeoCountry,
	GeoNodeType, GeoNode, GeoCity,
	GeoStreetType, GeoStreet
)
from geodata.models.timezones import TimeZone
from geodata.models.address import BaseAddress, Address


class TimeZoneModelTest(TestCase):
	def test_str_representation(self):
		tz = TimeZoneFactory(tz='Europe/Moscow', shift=3)
		self.assertIn('Europe/Moscow', str(tz))
		self.assertIn('UTC', str(tz))

	def test_by_utc_property(self):
		tz = TimeZoneFactory(shift=3)
		self.assertEqual(tz.by_utc, 'UTC+3')
		
		tz2 = TimeZoneFactory(shift=-5)
		self.assertEqual(tz2.by_utc, 'UTC-5')
		
		tz3 = TimeZoneFactory(shift=0)
		self.assertEqual(tz3.by_utc, 'UTC+0')


class GeoPartWorldModelTest(TestCase):
	def test_str_representation(self):
		part = GeoPartWorldFactory(name_ru='Евразия')
		self.assertEqual(str(part), 'Евразия')

	def test_wiki_data_url(self):
		part = GeoPartWorldFactory(wiki_data_id='Q46')
		self.assertIn('wikidata.org', part.wiki_data_url)
		self.assertIn('Q46', part.wiki_data_url)


class GeoRegionWorldModelTest(TestCase):
	def test_str_representation(self):
		region = GeoRegionWorldFactory(name_ru='Европа')
		self.assertEqual(str(region), 'Европа')

	def test_wiki_data_url(self):
		region = GeoRegionWorldFactory(wiki_data_id='Q46')
		self.assertIn('wikidata.org', region.wiki_data_url)


class GeoCountryModelTest(TestCase):
	def test_str_representation(self):
		country = GeoCountryFactory(name_ru='Россия')
		self.assertEqual(str(country), 'Россия')

	def test_population_density(self):
		country = GeoCountryFactory(area=17_000_000, population=146_000_000)
		density = country.population_density
		self.assertAlmostEqual(density, 146_000_000 / 17_000_000, places=2)

	def test_population_density_zero_area(self):
		country = GeoCountryFactory(area=0, population=1000)
		self.assertEqual(country.population_density, 0)

	def test_part_world_property(self):
		part = GeoPartWorldFactory()
		region = GeoRegionWorldFactory(part_world=part)
		country = GeoCountryFactory(region_world=region)
		self.assertEqual(country.part_world, part)

	def test_wiki_data_url(self):
		country = GeoCountryFactory(wiki_data_id='Q159')
		self.assertIn('wikidata.org', country.wiki_data_url)


class GeoNodeTypeModelTest(TestCase):
	def test_str_representation(self):
		node_type = GeoNodeTypeFactory(name_en='Region')
		self.assertIn('Region', str(node_type))


class GeoNodeModelTest(TestCase):
	def test_str_representation(self):
		country = GeoCountryFactory(name_ru='Россия')
		node = GeoNodeFactory(country=country, name_ru='Московская область')
		self.assertIn('Россия', str(node))
		self.assertIn('Московская область', str(node))

	def test_full_path_simple(self):
		country = GeoCountryFactory(name_ru='Россия')
		node = GeoNodeFactory(country=country, name_ru='Московская область')
		path = node.full_path
		self.assertIn('Россия', path)
		self.assertIn('Московская область', path)

	def test_full_path_with_parents(self):
		country = GeoCountryFactory(name_ru='Россия')
		parent = GeoNodeFactory(country=country, name_ru='Центральный федеральный округ')
		child = GeoNodeFactory(country=country, parent=parent, name_ru='Московская область')
		path = child.full_path
		self.assertIn('Россия', path)
		self.assertIn('Центральный федеральный округ', path)
		self.assertIn('Московская область', path)

	def test_name_with_type(self):
		node_type = GeoNodeTypeFactory(name_ru='Область')
		node = GeoNodeFactory(node_type=node_type, name_native='Московская')
		name_with_type = node.name_with_type
		self.assertIn('Область', name_with_type)
		self.assertIn('Московская', name_with_type)

	def test_name_with_type_always_returns_string(self):
		# node_type is required, so we test with a valid node_type
		node = GeoNodeFactory(name_native='Московская')
		# Should always return a string
		self.assertIsNotNone(node.name_with_type)
		self.assertIsInstance(node.name_with_type, str)

	def test_wiki_data_url(self):
		node = GeoNodeFactory(wiki_data_id='Q1697')
		self.assertIn('wikidata.org', node.wiki_data_url)

	def test_wiki_data_url_none(self):
		node = GeoNodeFactory(wiki_data_id=None)
		self.assertIsNone(node.wiki_data_url)


class GeoCityModelTest(TestCase):
	def test_str_representation(self):
		node = GeoNodeFactory(name_ru='Московская область')
		city = GeoCityFactory(node=node, name_ru='Москва')
		self.assertIn('Москва', str(city))
		self.assertIn('Московская область', str(city))

	def test_full_path(self):
		country = GeoCountryFactory(name_ru='Россия')
		node = GeoNodeFactory(country=country, name_ru='Московская область')
		city = GeoCityFactory(node=node, name_ru='Москва')
		path = city.full_path
		self.assertIn('Россия', path)
		self.assertIn('Московская область', path)
		self.assertIn('Москва', path)

	def test_wiki_data_url(self):
		city = GeoCityFactory(wiki_data_id='Q649')
		self.assertIn('wikidata.org', city.wiki_data_url)

	def test_wiki_data_url_none(self):
		city = GeoCityFactory(wiki_data_id=None)
		self.assertIsNone(city.wiki_data_url)


class GeoStreetTypeModelTest(TestCase):
	def test_str_representation(self):
		street_type = GeoStreetTypeFactory(short_ru='ул.', long_ru='улица')
		self.assertIn('ул.', str(street_type))
		self.assertIn('улица', str(street_type))


class GeoStreetModelTest(TestCase):
	def test_str_representation(self):
		city = GeoCityFactory(name_ru='Москва')
		street_type = GeoStreetTypeFactory(short_ru='ул.')
		street = GeoStreetFactory(city=city, street_type=street_type, name_native='Ленина')
		self.assertIn('ул.', str(street))
		self.assertIn('Ленина', str(street))
		self.assertIn('Москва', str(street))

	def test_name_with_type(self):
		street_type = GeoStreetTypeFactory(short_ru='ул.')
		street = GeoStreetFactory(street_type=street_type, name_native='Ленина')
		self.assertEqual(street.name_with_type, 'ул. Ленина')

	def test_name_lower_is_set_on_save(self):
		street = GeoStreetFactory(name_native='Тестовая')
		street.refresh_from_db()
		self.assertEqual(street.name_lower, 'тестовая')


class BaseAddressModelTest(TestCase):
	def test_str_representation(self):
		address = BaseAddressFactory()
		self.assertIsNotNone(str(address))
		self.assertIsNotNone(address.full_address)

	def test_full_address_generation(self):
		country = GeoCountryFactory(name_ru='Россия')
		node = GeoNodeFactory(country=country, name_ru='Московская область')
		city = GeoCityFactory(node=node, name_ru='Москва')
		street_type = GeoStreetTypeFactory(short_ru='ул.')
		street = GeoStreetFactory(city=city, street_type=street_type, name_native='Ленина')
		address = BaseAddressFactory(street=street, house='10', building='1')
		
		full = address.full_address
		self.assertIn('Россия', full)
		self.assertIn('Москва', full)
		self.assertIn('Ленина', full)
		self.assertIn('10', full)
		self.assertIn('1', full)

	def test_coordinates_property(self):
		# is_verified=True prevents geocoder from overwriting coordinates
		address = BaseAddressFactory(latitude=55.7558, longitude=37.6173, is_verified=True)
		coords = address.coordinates
		self.assertEqual(coords, (55.7558, 37.6173))

	def test_coordinates_none(self):
		# is_verified=True prevents geocoder from overwriting None coordinates
		address = BaseAddressFactory(latitude=None, longitude=None, is_verified=True)
		self.assertIsNone(address.coordinates)

	def test_save_sets_city_node_country(self):
		street = GeoStreetFactory()
		address = BaseAddressFactory.build(street=street)
		# Before save, these might not be set
		address.save()
		self.assertEqual(address.city, street.city)
		self.assertEqual(address.node, street.city.node)
		self.assertEqual(address.country, street.city.node.country)


class AddressModelTest(TestCase):
	def test_str_representation(self):
		address = AddressFactory()
		self.assertIsNotNone(str(address))
		self.assertIsNotNone(address.normal_address)

	def test_full_address_includes_apartment(self):
		address = AddressFactory(entrance=2, apartment=15)
		full = address.full_address
		self.assertIn('подъезд 2', full)
		self.assertIn('кв. 15', full)

	def test_full_address_includes_floor(self):
		address = AddressFactory(entrance=2, apartment=15, floor=5)
		full = address.full_address
		self.assertIn('этаж 5', full)

	def test_normal_address(self):
		base = BaseAddressFactory()
		address = AddressFactory(base=base, entrance=1, apartment=10)
		normal = address.full_address
		self.assertIn('подъезд 1', normal)
		self.assertIn('кв. 10', normal)

	def test_coordinates_from_base(self):
		# is_verified=True prevents geocoder from overwriting coordinates
		base = BaseAddressFactory(latitude=55.7558, longitude=37.6173, is_verified=True)
		address = AddressFactory(base=base)
		base.refresh_from_db()
		self.assertEqual(address.latitude, 55.7558)
		self.assertEqual(address.longitude, 37.6173)
		coords = address.coordinates
		self.assertEqual(coords, (55.7558, 37.6173))

