from django import template
from Shaurmania.settings import AVATARS_COUNT
import random

register = template.Library()

@register.filter( name='random_image_url' )
def random_image_url( value ):
	numbers = [ '{:03d}'.format(i) for i in range( 0, AVATARS_COUNT ) ]
	return '{}.png'.format( random.choice( numbers ) )
