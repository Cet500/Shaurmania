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


class TimeZoneFactoryTest(TestCase):
	def test_factory_creates_valid_object(self):
		tz = TimeZoneFactory()
		self.assertIsInstance(tz, TimeZone)
		self.assertTrue(tz.pk)
		self.assertTrue(tz.tz)
		self.assertIsNotNone(tz.shift)
		self.assertGreaterEqual(tz.shift, -12)
		self.assertLessEqual(tz.shift, 14)

	def test_str_and_by_utc(self):
		tz = TimeZoneFactory(shift=3)
		self.assertIn('UTC', str(tz))
		self.assertIn('UTC', tz.by_utc)


class GeoPartWorldFactoryTest(TestCase):
	def test_factory_creates_valid_object(self):
		part = GeoPartWorldFactory()
		self.assertIsInstance(part, GeoPartWorld)
		self.assertTrue(part.pk)
		self.assertTrue(part.name_ru)
		self.assertTrue(part.name_en)
		self.assertTrue(part.wiki_data_id)

	def test_str_and_wiki_url(self):
		part = GeoPartWorldFactory(name_ru='Евразия')
		self.assertEqual(str(part), 'Евразия')
		self.assertIn('wikidata.org', part.wiki_data_url)


class GeoRegionWorldFactoryTest(TestCase):
	def test_factory_creates_valid_object(self):
		region = GeoRegionWorldFactory()
		self.assertIsInstance(region, GeoRegionWorld)
		self.assertTrue(region.pk)
		self.assertIsNotNone(region.part_world)
		self.assertTrue(region.name_ru)
		self.assertTrue(region.name_en)

	def test_str_and_wiki_url(self):
		region = GeoRegionWorldFactory(name_ru='Европа')
		self.assertEqual(str(region), 'Европа')
		self.assertIn('wikidata.org', region.wiki_data_url)


class GeoCountryFactoryTest(TestCase):
	def test_factory_creates_valid_object(self):
		country = GeoCountryFactory()
		self.assertIsInstance(country, GeoCountry)
		self.assertTrue(country.pk)
		self.assertIsNotNone(country.region_world)
		self.assertTrue(country.name_ru)
		self.assertTrue(country.name_en)
		self.assertGreater(country.area, 0)
		self.assertGreater(country.population, 0)

	def test_str_and_properties(self):
		country = GeoCountryFactory(area=2_000_000, population=100_000_000)
		self.assertEqual(str(country), country.name_ru)
		self.assertEqual(country.population_density, 50)
		self.assertIsNotNone(country.part_world)
		self.assertIn('wikidata.org', country.wiki_data_url)


class GeoNodeTypeFactoryTest(TestCase):
	def test_factory_creates_valid_object(self):
		node_type = GeoNodeTypeFactory()
		self.assertIsInstance(node_type, GeoNodeType)
		self.assertTrue(node_type.pk)
		self.assertTrue(node_type.name_en)

	def test_str(self):
		node_type = GeoNodeTypeFactory(name_en='Region')
		self.assertIn('Region', str(node_type))


class GeoNodeFactoryTest(TestCase):
	def test_factory_creates_valid_object(self):
		node = GeoNodeFactory()
		self.assertIsInstance(node, GeoNode)
		self.assertTrue(node.pk)
		self.assertIsNotNone(node.country)
		self.assertIsNotNone(node.node_type)
		self.assertIsNotNone(node.timezone)
		self.assertTrue(node.name_ru)
		self.assertTrue(node.name_en)

	def test_str_and_properties(self):
		node = GeoNodeFactory(name_ru='Московская область')
		self.assertIn('Московская область', str(node))
		self.assertIn(node.country.name_ru, str(node))
		self.assertIsNotNone(node.full_path)
		self.assertIn(node.name_ru, node.full_path)

	def test_full_path_includes_parents(self):
		parent = GeoNodeFactory()
		child = GeoNodeFactory(parent=parent, country=parent.country)
		path = child.full_path
		self.assertIn(parent.name_ru, path)
		self.assertIn(child.name_ru, path)
		self.assertIn(child.country.name_ru, path)

	def test_name_with_type(self):
		node = GeoNodeFactory()
		name_with_type = node.name_with_type
		self.assertIsNotNone(name_with_type)
		self.assertIn(node.name_native, name_with_type)


class GeoCityFactoryTest(TestCase):
	def test_factory_creates_valid_object(self):
		city = GeoCityFactory()
		self.assertIsInstance(city, GeoCity)
		self.assertTrue(city.pk)
		self.assertIsNotNone(city.node)
		self.assertIsNotNone(city.timezone)
		self.assertTrue(city.name_ru)
		self.assertGreaterEqual(city.latitude, -90)
		self.assertLessEqual(city.latitude, 90)
		self.assertGreaterEqual(city.longitude, -180)
		self.assertLessEqual(city.longitude, 180)

	def test_str_and_properties(self):
		city = GeoCityFactory(name_ru='Москва')
		self.assertIn('Москва', str(city))
		self.assertIn(city.node.name_ru, str(city))
		self.assertIsNotNone(city.full_path)
		self.assertIn(city.name_ru, city.full_path)
		self.assertIn(city.node.country.name_ru, city.full_path)


class GeoStreetTypeFactoryTest(TestCase):
	def test_factory_creates_valid_object(self):
		street_type = GeoStreetTypeFactory()
		self.assertIsInstance(street_type, GeoStreetType)
		self.assertTrue(street_type.pk)
		self.assertTrue(street_type.short_ru)
		self.assertTrue(street_type.short_en)
		self.assertTrue(street_type.long_ru)
		self.assertTrue(street_type.long_en)
		self.assertIsInstance(street_type.variants_ru, list)
		self.assertIsInstance(street_type.variants_en, list)

	def test_str(self):
		street_type = GeoStreetTypeFactory(short_ru='ул.', long_ru='улица')
		self.assertIn('ул.', str(street_type))
		self.assertIn('улица', str(street_type))


class GeoStreetFactoryTest(TestCase):
	def test_factory_creates_valid_object(self):
		street = GeoStreetFactory()
		self.assertIsInstance(street, GeoStreet)
		self.assertTrue(street.pk)
		self.assertIsNotNone(street.city)
		self.assertIsNotNone(street.street_type)
		self.assertTrue(street.name_native)
		self.assertTrue(street.name_lower)

	def test_str_and_name_with_type(self):
		street = GeoStreetFactory(name_native='Ленина')
		self.assertIn('Ленина', str(street))
		self.assertIn(street.city.name_ru, str(street))
		self.assertIsNotNone(street.name_with_type)
		self.assertIn(street.name_native, street.name_with_type)

	def test_name_lower_is_set(self):
		street = GeoStreetFactory(name_native='Тестовая')
		self.assertEqual(street.name_lower, 'тестовая')


class BaseAddressFactoryTest(TestCase):
	def test_factory_creates_valid_object(self):
		address = BaseAddressFactory()
		self.assertIsInstance(address, BaseAddress)
		self.assertTrue(address.pk)
		self.assertIsNotNone(address.street)
		self.assertTrue(address.house)
		self.assertIsNotNone(address.city)
		self.assertIsNotNone(address.node)
		self.assertIsNotNone(address.country)

	def test_str_and_properties(self):
		address = BaseAddressFactory()
		self.assertIsNotNone(address.full_address)
		self.assertIn(address.country.name_ru, address.full_address)
		self.assertIn(address.house, address.full_address)

	def test_coordinates_property(self):
		address = BaseAddressFactory(latitude=55.7558, longitude=37.6173)
		coords = address.coordinates
		self.assertIsNotNone(coords)
		self.assertEqual(coords[0], 55.7558)
		self.assertEqual(coords[1], 37.6173)

	def test_coordinates_none_when_missing(self):
		# is_verified=True prevents geocoder from overwriting None coordinates
		address = BaseAddressFactory(latitude=None, longitude=None, is_verified=True)
		self.assertIsNone(address.coordinates)


class AddressFactoryTest(TestCase):
	def test_factory_creates_valid_object(self):
		address = AddressFactory()
		self.assertIsInstance(address, Address)
		self.assertTrue(address.pk)
		self.assertIsNotNone(address.base)
		self.assertGreaterEqual(address.entrance, 1)
		self.assertLessEqual(address.entrance, 40)
		self.assertGreaterEqual(address.apartment, 1)
		self.assertLessEqual(address.apartment, 32000)

	def test_str_and_properties(self):
		address = AddressFactory()
		self.assertIsNotNone(address.full_address)
		self.assertIn('подъезд', address.full_address)
		self.assertIn('кв.', address.full_address)
		self.assertIsNotNone(address.normal_address)

	def test_coordinates_from_base(self):
		# is_verified=True prevents geocoder from overwriting coordinates
		base = BaseAddressFactory(latitude=55.7558, longitude=37.6173, is_verified=True)
		address = AddressFactory(base=base)
		# Refresh to get latest values
		base.refresh_from_db()
		self.assertEqual(address.latitude, 55.7558)
		self.assertEqual(address.longitude, 37.6173)
		coords = address.coordinates
		self.assertIsNotNone(coords)
		self.assertEqual(coords[0], 55.7558)
		self.assertEqual(coords[1], 37.6173)

	def test_full_address_includes_apartment(self):
		address = AddressFactory(entrance=2, apartment=15, floor=5)
		full = address.full_address
		self.assertIn('подъезд 2', full)
		self.assertIn('кв. 15', full)
		self.assertIn('этаж 5', full)
