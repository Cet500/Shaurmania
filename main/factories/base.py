from faker import Faker

from Shaurmania.settings import TEST_FAKER_SEED


fake = Faker( 'ru_RU' )

if TEST_FAKER_SEED != -1:
	fake.seed( TEST_FAKER_SEED )
