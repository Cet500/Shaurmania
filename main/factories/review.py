from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from main.models import Review

from .base import fake
from .shaurma import ShaurmaFactory


class ReviewFactory( DjangoModelFactory ):
	class Meta:
		model = Review

	name    = LazyAttribute( lambda _: fake.first_name() )
	text    = LazyAttribute( lambda _: fake.text( max_nb_chars = 600 ) )
	stars   = LazyAttribute( lambda _: fake.random_int( 1, 5 ) )
	shaurma = SubFactory( ShaurmaFactory )

