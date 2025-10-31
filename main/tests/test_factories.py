from django.test import TestCase
from main.factories import (
    ShaurmaCategoryFactory,
    ShaurmaFactory,
    ShaurmaImageFactory,
    LocationFactory,
    UserFactory,
    AchievementFactory,
    UserAchievementFactory,
    ReviewFactory,
    StockFactory
)
from main.models import (
    ShaurmaCategory,
    Shaurma,
    ShaurmaImage,
    Location,
    User,
    Achievement,
    UserAchievement,
    Review,
    Stock,
    TIME_VARIANTS
)


class ShaurmaFactoryTest(TestCase):
    def test_factory_creates_valid_object(self):
        obj = ShaurmaFactory()
        self.assertIsInstance(obj, Shaurma)
        self.assertTrue(obj.pk)
        self.assertTrue(obj.name)
        self.assertIsNotNone(obj.category)
        self.assertGreater(obj.price, 0)
        self.assertGreater(obj.weight, 0)


class ShaurmaCategoryFactoryTest(TestCase):
    def test_factory_creates_valid_object(self):
        obj = ShaurmaCategoryFactory()
        self.assertIsInstance(obj, ShaurmaCategory)
        self.assertTrue(obj.pk)
        self.assertTrue(obj.name)


class ShaurmaImageFactoryTest(TestCase):
    def test_factory_creates_valid_object(self):
        obj = ShaurmaImageFactory()
        self.assertIsInstance(obj, ShaurmaImage)
        self.assertTrue(obj.pk)
        self.assertIsNotNone(obj.shaurma)
        self.assertTrue(bool(getattr(obj.image, 'name', '')))


class LocationFactoryTest(TestCase):
    def test_factory_creates_valid_object(self):
        obj = LocationFactory()
        self.assertIsInstance(obj, Location)
        self.assertTrue(obj.pk)
        self.assertIn(obj.timeline, tuple(TIME_VARIANTS.keys()))


class UserFactoryTest(TestCase):
    def test_factory_creates_valid_object_and_sets_password(self):
        obj = UserFactory(password='secret123')
        self.assertIsInstance(obj, User)
        self.assertTrue(obj.pk)
        self.assertTrue(obj.check_password('secret123'))


class AchievementFactoryTest(TestCase):
    def test_factory_creates_valid_object(self):
        obj = AchievementFactory()
        self.assertIsInstance(obj, Achievement)
        self.assertTrue(obj.pk)


class UserAchievementFactoryTest(TestCase):
    def test_factory_creates_valid_object(self):
        obj = UserAchievementFactory()
        self.assertIsInstance(obj, UserAchievement)
        self.assertTrue(obj.pk)
        self.assertIsNotNone(obj.user)
        self.assertIsNotNone(obj.achievement)


class ReviewFactoryTest(TestCase):
    def test_factory_creates_valid_object(self):
        obj = ReviewFactory()
        self.assertIsInstance(obj, Review)
        self.assertTrue(obj.pk)
        self.assertGreaterEqual(obj.stars, 1)
        self.assertLessEqual(obj.stars, 5)


class StockFactoryTest(TestCase):
    def test_factory_creates_valid_object_with_categories(self):
        obj = StockFactory()
        self.assertIsInstance(obj, Stock)
        self.assertTrue(obj.pk)
        self.assertGreaterEqual(obj.categories.count(), 1)

    def test_factory_respects_explicit_categories(self):
        cats = [ShaurmaCategoryFactory() for _ in range(2)]
        obj = StockFactory(categories=cats)
        self.assertEqual(obj.categories.count(), 2)
