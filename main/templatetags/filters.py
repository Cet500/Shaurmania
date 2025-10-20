from django import template
import random

register = template.Library()

@register.filter(name='random_image_url')
def random_image_url(value):
    numbers = ['{:03d}'.format(i) for i in range(0,57)]
    return '{}.png'.format(random.choice(numbers))
