from django.test import TestCase
from django.core.exceptions import ValidationError

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
from main.models import Shaurma, User, Achievement


class ShaurmaModelTest(TestCase):
    def test_slug_is_generated_and_str(self):
        shaurma = ShaurmaFactory(name="ОченьВкуснаяШаурма")
        self.assertTrue(shaurma.slug)
        self.assertIn("ОченьВкуснаяШаурма", str(shaurma))

    def test_picture_is_saved(self):
        shaurma = ShaurmaFactory()
        self.assertTrue(bool(getattr(shaurma.picture, "name", "")))


class ShaurmaCategoryModelTest(TestCase):
    def test_str(self):
        cat = ShaurmaCategoryFactory(name="Классика")
        self.assertEqual(str(cat), "Классика")
    
    def test_fields_basic(self):
        cat = ShaurmaCategoryFactory()
        self.assertIsInstance(cat.description, str)
        self.assertIsInstance(cat.order, int)


class ShaurmaImageModelTest(TestCase):
    def test_relations_and_str(self):
        img = ShaurmaImageFactory()
        self.assertIsInstance(img.shaurma, Shaurma)
        self.assertIn(img.shaurma.name, str(img))


class LocationModelTest(TestCase):
    def test_slug_is_generated_and_str(self):
        loc = LocationFactory(name="Главный филиал")
        self.assertTrue(loc.slug)
        self.assertEqual(str(loc), "Главный филиал")


class UserModelTest(TestCase):
    def test_str_and_flags_defaults(self):
        user = UserFactory(username="testuser", email="t@example.com")
        self.assertIn("testuser", str(user))
        self.assertIn("t@example.com", str(user))
        self.assertTrue(user.is_active)


class AchievementModelTest(TestCase):
    def test_str(self):
        ach = AchievementFactory(name="Первый заказ")
        self.assertEqual(str(ach), "Первый заказ")


class UserAchievementModelTest(TestCase):
    def test_relations_and_str(self):
        ua = UserAchievementFactory()
        self.assertIsInstance(ua.user, User)
        self.assertIsInstance(ua.achievement, Achievement)
        self.assertIn(ua.user.username, str(ua))
        self.assertIn(ua.achievement.name, str(ua))
    
    def test_auto_date_set(self):
        ua = UserAchievementFactory()
        self.assertIsNotNone(ua.get_date)


class ReviewModelTest(TestCase):
    def test_limits_and_str(self):
        review = ReviewFactory(stars=5)
        self.assertGreaterEqual(review.stars, 1)
        self.assertLessEqual(review.stars, 5)
        self.assertIn("5", str(review))
    
    def test_stars_validator_enforced(self):
        review = ReviewFactory.build(stars=6)
        with self.assertRaises(ValidationError):
            review.full_clean()


class StockModelTest(TestCase):
    def test_slug_categories_and_str(self):
        stock = StockFactory(name="Скидка дня")
        self.assertTrue(stock.slug)
        self.assertGreaterEqual(stock.categories.count(), 1)
        self.assertEqual(str(stock), "Скидка дня")
    
    def test_discount_and_dates(self):
        stock = StockFactory()
        self.assertGreaterEqual(stock.discount, 0)
        self.assertLessEqual(stock.discount, 100)
        self.assertLessEqual(stock.date_start, stock.date_end)
