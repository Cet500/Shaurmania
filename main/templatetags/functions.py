from django_jinja import library
from Shaurmania.settings import AVATARS_COUNT
import random


@library.global_function()
def random_image_url():
	numbers = [ '{:03d}'.format(i) for i in range( 0, AVATARS_COUNT ) ]
	return '{}.png'.format( random.choice( numbers ) )