from django.test import TestCase
from main.factories import (
    AchievementFactory,
    DeliveryFactory,
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
from main.models import (
    Achievement,
    Delivery,
    Location,
    News,
    NewsTag,
    Review,
    Shaurma,
    ShaurmaCategory,
    ShaurmaImage,
    Stock,
    TIME_VARIANTS,
    User,
    UserAchievement,
    UserAddress,
    UserAvatar,
    UserSocialLink,
)
from main.models.delivery import SPEED_TYPES


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


class NewsTagFactoryTest(TestCase):
    def test_factory_creates_valid_tag(self):
        tag = NewsTagFactory()
        self.assertIsInstance(tag, NewsTag)
        self.assertTrue(tag.pk)


class NewsFactoryTest(TestCase):
    def test_factory_assigns_tags(self):
        tag = NewsTagFactory()
        news = NewsFactory(tags=[tag])
        self.assertIsInstance(news, News)
        self.assertTrue(news.slug)
        self.assertTrue(news.tags.filter(pk=tag.pk).exists())


class UserAvatarFactoryTest(TestCase):
    def test_factory_creates_avatar(self):
        avatar = UserAvatarFactory()
        self.assertIsInstance(avatar, UserAvatar)
        self.assertTrue(avatar.pk)
        self.assertIsNotNone(avatar.avatar)


class UserSocialLinkFactoryTest(TestCase):
    def test_factory_creates_verified_link(self):
        link = UserSocialLinkFactory()
        link.full_clean()
        self.assertIsInstance(link, UserSocialLink)
        self.assertTrue(link.pk)
        self.assertTrue(link.is_verified)


class UserAddressFactoryTest(TestCase):
    def test_factory_creates_valid_object(self):
        address = UserAddressFactory()
        self.assertIsInstance(address, UserAddress)
        self.assertTrue(address.pk)
        self.assertIsNotNone(address.user)
        self.assertIsNotNone(address.address)


class DeliveryFactoryTest(TestCase):
    def test_factory_creates_valid_object(self):
        delivery = DeliveryFactory()
        self.assertIsInstance(delivery, Delivery)
        self.assertTrue(delivery.pk)
        self.assertIsNotNone(delivery.city)
        self.assertGreaterEqual(delivery.delivery_price, 0)
        self.assertIn(delivery.delivery_speed, tuple(SPEED_TYPES.keys()))
