from django.test import TestCase
from django.conf import settings

from main.factories import (
    ShaurmaFactory,
    ShaurmaImageFactory,
    LocationFactory,
    AchievementFactory,
)


class MediaGenerationTest(TestCase):
    def test_media_root_is_test_media(self):
        self.assertTrue(str(settings.MEDIA_ROOT).endswith('test_media'))

    def test_shaurma_picture_saved_and_thumbnails(self):
        obj = ShaurmaFactory()
        self.assertTrue(bool(getattr(obj.picture, 'name', '')))

        self.assertTrue(obj.thumbnail_md.url)
        self.assertTrue(obj.thumbnail_sm.url)

    def test_shaurma_image_saved_and_thumbnail(self):
        img = ShaurmaImageFactory()
        self.assertTrue(bool(getattr(img.image, 'name', '')))
        img.thumbnail_md.generate()
        self.assertTrue(img.thumbnail_md.url)

    def test_location_picture_saved(self):
        loc = LocationFactory()
        self.assertTrue(bool(getattr(loc.picture, 'name', '')))

    def test_achievement_picture_saved(self):
        ach = AchievementFactory()
        self.assertTrue(bool(getattr(ach.picture, 'name', '')))


