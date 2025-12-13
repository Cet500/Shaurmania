import factory
from factory.django import DjangoModelFactory
from geodata.models import TimeZone


class TimeZoneFactory(DjangoModelFactory):
    class Meta:
        model = TimeZone
        django_get_or_create = ['tz']

    tz    = factory.Faker( 'timezone' )
    shift = factory.Faker( 'pyint', min_value = -12, max_value = 14 )
