from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory, ImageField

from main.models import Achievement, UserAchievement

from .base import fake
from .user import UserFactory


class AchievementFactory( DjangoModelFactory ):
	class Meta:
		model = Achievement

	name    = LazyAttribute( lambda _: fake.word() )
	picture = ImageField( width = 300, height = 300, color = 'white' )


class UserAchievementFactory( DjangoModelFactory ):
	class Meta:
		model = UserAchievement

	user        = SubFactory( UserFactory )
	achievement = SubFactory( AchievementFactory )
