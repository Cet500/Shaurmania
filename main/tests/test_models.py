from django.core.exceptions import ValidationError
from django.templatetags.static import static
from django.test import TestCase

from main.factories import (
    AchievementFactory,
    LocationFactory,
    NewsFactory,
    NewsTagFactory,
    ReviewFactory,
    ShaurmaCategoryFactory,
    ShaurmaFactory,
    ShaurmaImageFactory,
    StockFactory,
    UserAchievementFactory,
    UserAddressFactory,
    UserAvatarFactory,
    UserFactory,
    UserSocialLinkFactory,
)
from main.models import Achievement, Delivery, News, NewsTag, Shaurma, User
from main.models.user import UserAddress, UserAvatar, UserSocialLink
from main.factories import DeliveryFactory


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

    def test_avatar_uses_default_when_missing(self):
        user = UserFactory()
        self.assertEqual(user.avatar_48_url, static('main/img/avatar/avatar_015.png'))

    def test_avatar_uses_primary_avatar(self):
        user = UserFactory()
        avatar = UserAvatarFactory(user=user, is_primary=True)
        self.assertEqual(user.avatar_48_url, avatar.avatar_48x.url)


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


class NewsTagModelTest(TestCase):
    def test_slug_is_generated(self):
        tag = NewsTagFactory(name="Горячее")
        self.assertTrue(tag.slug)
        self.assertEqual(str(tag), "Горячее")


class NewsModelTest(TestCase):
    def test_slug_and_tags(self):
        tag = NewsTagFactory(name="Срочно")
        news = NewsFactory(title="Большое открытие", tags=[tag])
        self.assertTrue(news.slug)
        self.assertTrue(news.tags.filter(pk=tag.pk).exists())
        self.assertEqual(str(news), "Большое открытие")


class UserSocialLinkModelTest(TestCase):
    def test_clean_sets_verified(self):
        link = UserSocialLinkFactory(network='TG', link='https://t.me/testchannel')
        link.full_clean()
        self.assertTrue(link.is_verified)
        self.assertIn('TG', str(link))


class UserAddressModelTest(TestCase):
    def test_str_and_defaults(self):
        address = UserAddressFactory()

        self.assertIsNotNone(address.user)
        self.assertIsNotNone(address.address)

        self.assertIn(address.user.username, str(address))
        self.assertIn(str(address.address), str(address))

    def test_display_title(self):
        address = UserAddressFactory(title="Дом")
        self.assertEqual(address.display_title, "Дом")

    def test_is_default_constraint(self):
        user = UserFactory()
        addr1 = UserAddressFactory(user=user, is_default=True)
        addr2 = UserAddressFactory(user=user, is_default=True)

        addr1.refresh_from_db()
        addr2.refresh_from_db()

        defaults = UserAddress.objects.filter(user=user, is_default=True)
        self.assertEqual(defaults.count(), 1)
        self.assertIn(defaults.first(), [addr1, addr2])


class DeliveryModelTest(TestCase):
    def test_str_and_relations(self):
        delivery = DeliveryFactory()
        self.assertIsInstance(delivery, Delivery)
        self.assertIsNotNone(delivery.city)
        self.assertGreaterEqual(delivery.delivery_price, 0)
        from main.models.delivery import SPEED_TYPES
        self.assertIn(delivery.delivery_speed, tuple(SPEED_TYPES.keys()))
