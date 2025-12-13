from django.db import models as m
from django.core.validators import MinValueValidator, MaxValueValidator

from geodata.services import Geocoder


class BaseAddress( m.Model ):
	street  = m.ForeignKey( 'GeoStreet', on_delete = m.PROTECT, verbose_name = 'Улица' )

	# Денормализация данных
	city    = m.ForeignKey( 'GeoCity', on_delete = m.PROTECT, verbose_name = 'Город',
	                        editable = False )
	node    = m.ForeignKey( 'GeoNode', on_delete = m.PROTECT, verbose_name = 'Регион',
	                        editable = False )
	country = m.ForeignKey( 'GeoCountry', on_delete = m.PROTECT, verbose_name = 'Страна',
	                        editable = False )

	house    = m.CharField( max_length = 30, db_index = True, verbose_name = 'Дом/Здание' )
	building = m.CharField( max_length = 10, blank = True, verbose_name = 'Корпус/Строение' )

	postal_code    = m.CharField( blank = True, null = True, max_length = 10, verbose_name = 'Почтовый индекс' )

	full_address   = m.CharField( max_length = 500, blank = True, null = True, editable = False,
	                            verbose_name = 'Полный адрес' )
	normal_address = m.CharField( max_length = 500, blank = True, null = True, editable = False,
	                              verbose_name = 'Полный нормализованный адрес' )

	latitude  = m.FloatField(
		verbose_name = 'Широта', blank = True, null = True,
		validators = [ MinValueValidator( -90.0 ), MaxValueValidator( 90.0 ) ]
	)
	longitude = m.FloatField(
		verbose_name = 'Долгота', blank = True, null = True,
		validators = [ MinValueValidator( -180.0 ), MaxValueValidator( 180.0 ) ]
	)

	is_verified = m.BooleanField( default = False, verbose_name = 'Подтверждён' )

	created_at = m.DateTimeField( auto_now_add = True, verbose_name = 'Дата/время записи' )
	updated_at = m.DateTimeField( auto_now = True, verbose_name = 'Дата/время изменения' )

	@property
	def coordinates( self ):
		"""Координаты как tuple"""
		if self.latitude and self.longitude:
			return (float( self.latitude ), float( self.longitude ))
		return None

	def __str__(self):
		return self.full_address

	def save( self, *args, **kwargs ):
		if not self.city_id:
			self.city = self.street.city
		if not self.node_id:
			self.node = self.street.city.node
		if not self.country_id:
			self.country = self.street.city.node.country

		self.full_address = self._generate_full_address()

		if not self.is_verified:
			geocoder = Geocoder( self.full_address )
			geo = geocoder.get_geo_object()

			if geo:
				# formatted
				formatted = geocoder.get_formatted_address()
				if formatted:
					self.normal_address = formatted

				# coords
				coords = geocoder.get_coordinates()
				if coords:
					self.latitude, self.longitude = coords

				# индекс
				meta = geo.get( 'metaDataProperty', { } ).get( 'GeocoderMetaData', { } )
				addr = meta.get( 'Address', { } )
				if addr.get( 'postal_code' ):
					self.postal_code = addr['postal_code']

				self.is_verified = True

		super().save( *args, **kwargs )

	def _generate_full_address( self ):
		"""Генерация полного адреса из связанных данных."""
		parts = [
			self.country.name_ru,
			self.node.name_with_type,
			f"г. {self.city.name_ru}",
			self.street.name_with_type,
		]

		house_str = f"д. {self.house}"
		if self.building:
			house_str += f" корп. {self.building}"
		parts.append( house_str )

		return ", ".join(parts)

	class Meta:
		verbose_name = 'базовый адрес'
		verbose_name_plural = '6. Базовые адреса'
		db_table = 'base_addresses'
		ordering = ['-updated_at']
		indexes = [
			m.Index( fields = ['full_address'] ),
			m.Index( fields = ['latitude', 'longitude'] ),
		]
		constraints = [
			m.UniqueConstraint(
				fields = ['street', 'house', 'building'],
				name = 'unique_physical_address'
			)
		]


class Address( m.Model ):
	base = m.ForeignKey(
        BaseAddress, on_delete = m.PROTECT, db_index = True,
        related_name = 'addresses', verbose_name = 'Базовый адрес'
    )

	entrance  = m.PositiveSmallIntegerField(
		verbose_name = 'Подъезд',
	    validators = [ MinValueValidator( 1 ), MaxValueValidator( 40 ) ]
	)
	floor     = m.PositiveSmallIntegerField(
		blank = True, null=True, verbose_name = 'Этаж',
		validators = [ MinValueValidator( 1 ), MaxValueValidator( 250 ) ]
	)
	apartment = m.PositiveSmallIntegerField(
		verbose_name = 'Квартира/Офис',
		validators = [ MinValueValidator( 1 ), MaxValueValidator( 32000 ) ]
	)
	intercom  = m.PositiveSmallIntegerField(
		blank = True, null=True, verbose_name = 'Домофон',
		validators = [ MinValueValidator( 1 ), MaxValueValidator( 32000 ) ]
	)

	is_active  = m.BooleanField( default = True, verbose_name = 'Активен' )

	created_at = m.DateTimeField( auto_now_add = True, verbose_name = 'Дата/время записи' )
	updated_at = m.DateTimeField( auto_now = True, verbose_name = 'Дата/время изменения' )

	@property
	def latitude( self ):
		return self.base.latitude

	@property
	def longitude( self ):
		return self.base.longitude

	@property
	def coordinates( self ):
		"""Координаты как tuple"""
		return ( self.latitude, self.longitude )

	@property
	def full_address( self ) -> str:
		"""Полный адрес с подъездом/квартирой (на базе нормализованного)."""
		base_str = self.base.full_address

		if not base_str:
			return ''

		parts = [ base_str ]

		parts.append( f'подъезд {self.entrance}' )

		if self.floor:
			parts.append( f'этаж {self.floor}' )

		parts.append( f'кв. {self.apartment}' )

		return ', '.join( parts )

	@property
	def normal_address( self ) -> str:
		"""Полный адрес с подъездом/квартирой (на базе нормализованного)."""
		base_str = self.base.normal_address

		if not base_str:
			return ''

		parts = [
			base_str,
			f'подъезд {self.entrance}',
			f'кв. {self.apartment}'
		]

		return ', '.join( parts )

	def __str__(self):
		return self.normal_address

	class Meta:
		verbose_name = 'адрес'
		verbose_name_plural = '7. Адреса'
		db_table = 'addresses'
		ordering = ['-updated_at']
		constraints = [
			m.UniqueConstraint(
				fields = ['base', 'entrance', 'apartment'],
				name = 'unique_flat_in_base_address',
			),
		]
