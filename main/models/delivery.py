from django.db import models as m


SPEED_TYPES = {
	'XS': 'Очень медленно',
	'S' : 'Meдленно',
	'M' : 'Средне',
	'F' : 'Быстро',
	'EF': 'Очень быстро'
}

class Delivery( m.Model ):
	"""Доставка в городах"""
	city = m.ForeignKey( 'geodata.GeoCity', on_delete = m.CASCADE, verbose_name = 'Город' )

	delivery_price = m.IntegerField( default = 0, verbose_name = 'Стоимость доставки' )
	delivery_speed = m.CharField( max_length = 2, choices = SPEED_TYPES, default = 'M',
	                              verbose_name = 'Скорость доставки' )

	created_at = m.DateTimeField( auto_now_add = True, db_index = True, verbose_name = 'Дата/время записи' )
	updated_at = m.DateTimeField( auto_now = True, verbose_name = 'Дата/время изменения' )

	class Meta:
		verbose_name = 'доставка в города'
		verbose_name_plural = 'доставка в города'
		ordering = [ 'city' ]
