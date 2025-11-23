from factory import LazyAttribute, SubFactory, post_generation
from factory.django import DjangoModelFactory, ImageField
from faker import Faker
from Shaurmania.settings import TEST_FAKER_SEED
from main.models import (
	Shaurma,
	ShaurmaCategory,
	ShaurmaImage,
	Location,
	User,
	Achievement,
	UserAchievement,
	Review,
	Stock,
	TIME_VARIANTS,
)


fake = Faker( 'ru_RU' )

if TEST_FAKER_SEED != -1:
	fake.seed( TEST_FAKER_SEED )


class ShaurmaCategoryFactory(DjangoModelFactory):
	class Meta:
		model = ShaurmaCategory

	name        = LazyAttribute( lambda _: fake.word() )
	description = LazyAttribute( lambda _: fake.text( max_nb_chars = 200 ) )
	order       = LazyAttribute( lambda _: fake.random_int( 0, 10 ) )


class ShaurmaFactory(DjangoModelFactory):
	class Meta:
		model = Shaurma

	name        = LazyAttribute( lambda _: fake.word() )
	category    = SubFactory( ShaurmaCategoryFactory )
	compound    = LazyAttribute( lambda _: fake.text( max_nb_chars = 600 ) )
	short_text  = LazyAttribute( lambda _: fake.text( max_nb_chars = 200 ) )
	description = LazyAttribute( lambda _: fake.text( max_nb_chars = 1000 ) )
	picture     = ImageField( width = 300, height = 300, color = 'white' )
	price       = LazyAttribute( lambda _: fake.random_int( 100, 900 ) )
	weight      = LazyAttribute( lambda _: fake.random_int( 400, 600 ) )


class ShaurmaImageFactory(DjangoModelFactory):
	class Meta:
		model = ShaurmaImage

	shaurma = SubFactory( ShaurmaFactory )
	image   = ImageField( width = 300, height = 300, color = 'white' )
	caption = LazyAttribute( lambda _: fake.sentence( nb_words = 3 ) )
	order   = LazyAttribute( lambda _: fake.random_int( 0, 10 ) )


class LocationFactory(DjangoModelFactory):
	class Meta:
		model = Location

	name        = LazyAttribute( lambda _: fake.word() )
	description = LazyAttribute( lambda _: fake.text( max_nb_chars = 600 ) )
	planet      = LazyAttribute( lambda _: fake.word() )
	country     = LazyAttribute( lambda _: fake.country() )
	city        = LazyAttribute( lambda _: fake.city() )
	address     = LazyAttribute( lambda _: fake.address() )
	picture     = ImageField( width = 300, height = 300, color = 'white' )
	timeline    = LazyAttribute( lambda _: fake.random_element( elements = tuple( TIME_VARIANTS.keys() ) ) )
	contacts    = LazyAttribute( lambda _: fake.phone_number() )
	open_hours  = LazyAttribute( lambda _: fake.time() )
	close_hours = LazyAttribute( lambda _: fake.time() )


class UserFactory(DjangoModelFactory):
	class Meta:
		model = User

	name         = LazyAttribute( lambda _: fake.name() )
	username     = LazyAttribute( lambda _: fake.user_name() )
	avatar       = ImageField( width = 128, height = 128, color = 'blue' )
	email        = LazyAttribute( lambda _: fake.email() )
	phone        = LazyAttribute( lambda _: fake.phone_number() )
	last_address = LazyAttribute( lambda _: fake.address() )

	@classmethod
	def _create(cls, model_class, *args, **kwargs):
		password = kwargs.pop('password', fake.password(length=10))

		user = super()._create(model_class, *args, **kwargs)
		user.set_password(password)
		user.save()

		return user


class AchievementFactory(DjangoModelFactory):
	class Meta:
		model = Achievement

	name    = LazyAttribute( lambda _: fake.word() )
	picture = ImageField( width = 300, height = 300, color = 'white' )


class UserAchievementFactory(DjangoModelFactory):
	class Meta:
		model = UserAchievement

	user        = SubFactory( UserFactory )
	achievement = SubFactory( AchievementFactory )


class ReviewFactory(DjangoModelFactory):
	class Meta:
		model = Review

	name    = LazyAttribute( lambda _: fake.first_name() )
	text    = LazyAttribute( lambda _: fake.text( max_nb_chars = 600 ) )
	stars   = LazyAttribute( lambda _: fake.random_int( 1, 5 ) )
	shaurma = SubFactory( ShaurmaFactory )


class StockFactory(DjangoModelFactory):
	class Meta:
		model = Stock

	name        = LazyAttribute( lambda _: fake.word() )
	short_text  = LazyAttribute( lambda _: fake.text( max_nb_chars = 160 ) )
	description = LazyAttribute( lambda _: fake.text( max_nb_chars = 1000 ) )
	condition   = LazyAttribute( lambda _: fake.text( max_nb_chars = 1000 ) )
	image       = ImageField( width = 300, height = 300, color = 'white' )
	discount    = LazyAttribute( lambda _: fake.random_int( 5, 95 ) )
	date_start  = LazyAttribute( lambda _: fake.date_between( start_date = '-30d', end_date = 'today' ) )
	date_end    = LazyAttribute( lambda o: fake.date_between( start_date = o.date_start, end_date = '+30d' ) )

	@classmethod
	def _create( cls, model_class, *args, **kwargs ):
		categories = kwargs.pop( 'categories', [ ShaurmaCategoryFactory() for _ in range( fake.random_int( 1, 3 ) ) ] )
		stock = super()._create( model_class, *args, **kwargs )
		
		if categories:
			stock.categories.set( categories )
   
		return stock

