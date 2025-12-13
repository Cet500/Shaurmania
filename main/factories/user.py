from factory import LazyAttribute, Sequence, SubFactory
from factory.django import DjangoModelFactory, ImageField

from main.models import User
from main.models.user import UserAvatar, UserSocialLink, UserAddress

from .base import fake
from geodata.factories import AddressFactory


def _social_network():
	return fake.random_element( elements = tuple( {'TG', 'GH', 'VK', 'IG', 'LN'} ) )


def _build_social_link( network: str ) -> str:
	slug = fake.pystr( min_chars = 5, max_chars = 10 ).lower()
	templates = {
		'TG': f'https://t.me/{slug}',
		'GH': f'https://github.com/{slug}',
		'VK': f'https://vk.com/{slug}',
		'IG': f'https://www.instagram.com/{slug}/',
		'LN': f'https://www.linkedin.com/in/{slug}/',
	}
	return templates.get( network, f'https://t.me/{slug}' )


class UserFactory( DjangoModelFactory ):
	class Meta:
		model = User

	name         = LazyAttribute( lambda _: fake.first_name() )
	lastname     = LazyAttribute( lambda _: fake.last_name() )
	username     = Sequence( lambda n: f'user{n}' )
	email        = Sequence( lambda n: f'user{n}@example.com' )
	phone        = LazyAttribute( lambda _: fake.msisdn() )
	last_address = LazyAttribute( lambda _: fake.address() )

	@classmethod
	def _create( cls, model_class, *args, **kwargs ):
		password = kwargs.pop( 'password', fake.password( length = 10 ) )
		user = super()._create( model_class, *args, **kwargs )
		user.set_password( password )
		user.save()
		return user


class UserAvatarFactory( DjangoModelFactory ):
	class Meta:
		model = UserAvatar

	user = SubFactory( UserFactory )
	avatar = ImageField( width = 256, height = 256, color = 'white' )
	is_primary = False


class UserSocialLinkFactory( DjangoModelFactory ):
	class Meta:
		model = UserSocialLink

	user        = SubFactory( UserFactory )
	network     = LazyAttribute( lambda _: _social_network() )
	link        = LazyAttribute( lambda o: _build_social_link( o.network ) )
	description = LazyAttribute( lambda _: fake.sentence( nb_words = 6 ) )
	is_shown    = LazyAttribute( lambda _: fake.boolean() )


class UserAddressFactory( DjangoModelFactory ):
	class Meta:
		model = UserAddress

	user      = SubFactory( UserFactory )
	address   = SubFactory( AddressFactory )
	title     = LazyAttribute( lambda _: fake.random_element( elements = ('Дом', 'Работа', 'Офис', 'Дача', None) ) )
	notes     = LazyAttribute( lambda _: fake.text( max_nb_chars = 200 ) if fake.boolean() else None )
	is_default = LazyAttribute( lambda _: fake.boolean() )


