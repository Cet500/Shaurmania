from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models as m


class GeoPartWorld( m.Model ):
	"""Континент света"""
	name_ru = m.CharField( max_length = 20, unique = True, verbose_name = 'Название RUS', db_index = True )
	name_en = m.CharField( max_length = 20, unique = True, verbose_name = 'Название ENG' )

	wiki_data_id = m.CharField( max_length = 20, unique = True, verbose_name = 'Wikipedia ID' )

	@property
	def wiki_data_url( self ):
		return f'https://www.wikidata.org/wiki/{self.wiki_data_id}'

	def __str__( self ):
		return self.name_ru

	class Meta:
		verbose_name = 'часть света'
		verbose_name_plural = '0. Части света'
		db_table = 'geo_parts_world'
		ordering = ['id']


class GeoRegionWorld(m.Model):
	"""Регионы мира"""
	part_world = m.ForeignKey( GeoPartWorld, on_delete = m.PROTECT,
	                           related_name = 'regions_world', verbose_name = 'Часть света' )

	name_ru = m.CharField( max_length = 50, unique = True, verbose_name = 'Название RUS', db_index = True )
	name_en = m.CharField( max_length = 50, unique = True, verbose_name = 'Название ENG' )

	wiki_data_id = m.CharField( max_length = 20, unique = True, verbose_name = 'Wikipedia ID' )

	@property
	def wiki_data_url( self ):
		return f'https://www.wikidata.org/wiki/{self.wiki_data_id}'

	def __str__( self ):
		return self.name_ru

	class Meta:
		verbose_name = 'регион мира'
		verbose_name_plural = '1. Регионы мира'
		db_table = 'geo_regions_world'
		ordering = ['id']


class GeoCountry( m.Model ):
	"""Страна"""
	region_world     = m.ForeignKey( GeoRegionWorld, on_delete = m.PROTECT,
	                                 related_name = 'countries', verbose_name = 'Регион мира' )

	name_ru          = m.CharField( max_length = 100, unique = True, verbose_name = 'Название RUS', db_index = True )
	name_official_ru = m.CharField( max_length = 150, verbose_name = 'Название (офф) RUS' )
	name_en          = m.CharField( max_length = 100, unique = True, verbose_name = 'Название ENG', db_index = True )
	name_official_en = m.CharField( max_length = 150, verbose_name = 'Название (офф) ENG' )

	capital_ru       = m.CharField( max_length = 40, verbose_name = 'Столица RUS' )
	capital_en       = m.CharField( max_length = 40, verbose_name = 'Столица ENG' )

	emoji_code       = m.CharField( max_length = 5, blank = True, null = True, verbose_name = 'Код' )
	emoji_flag       = m.CharField( max_length = 5, blank = True, null = True, verbose_name = 'Флажок' )
	flag             = m.FileField( upload_to = 'geo/flags', blank = True, null = True,
	                                validators = [FileExtensionValidator( ['svg'] )],
	                                verbose_name = 'Флаг SVG' )

	currency_code    = m.CharField( max_length = 3,  blank = True, null = True, verbose_name = 'Код валюты' )
	currency_name    = m.CharField( max_length = 50, blank = True, null = True, verbose_name = 'Название валюты' )
	currency_symbol  = m.CharField( max_length = 5,  blank = True, null = True, verbose_name = 'Символ валюты' )

	phone_code       = m.CharField( max_length = 4, blank = True, null = True, verbose_name = 'Код телефона' )
	cca2             = m.CharField( max_length = 2, blank = True, null = True, verbose_name = '2букв код страны' )
	cca3             = m.CharField( max_length = 3, blank = True, null = True, verbose_name = '3букв код страны' )
	ccn3             = m.CharField( max_length = 3, blank = True, null = True, verbose_name = '3знач код страны' )
	top_level_domain = m.CharField( max_length = 5, blank = True, null = True, verbose_name = 'Код домена' )

	is_landlocked    = m.BooleanField( default = False, verbose_name = 'Только суша?' )
	is_independent   = m.BooleanField( default = True, verbose_name = 'Страна независима?' )
	is_member_oon    = m.BooleanField( default = True, verbose_name = 'Входит в ООН?' )

	area             = m.PositiveBigIntegerField( verbose_name = 'Площадь' )
	population       = m.PositiveBigIntegerField( verbose_name = 'Население' )

	latitude         = m.FloatField(
		verbose_name = 'Широта центра',
		validators = [MinValueValidator( -90.0 ), MaxValueValidator( 90.0 )]
	)
	longitude        = m.FloatField(
		verbose_name = 'Долгота центра',
		validators = [MinValueValidator( -180.0 ), MaxValueValidator( 180.0 )]
	)

	wiki_data_id     = m.CharField( max_length = 20, unique = True, verbose_name = 'Wikipedia ID' )

	is_handly_verify = m.BooleanField( default = False, verbose_name = 'Проверено вручную' )

	datetime_create  = m.DateTimeField( auto_now_add = True, db_index = True, verbose_name = 'Дата/время записи' )
	datetime_edit    = m.DateTimeField( auto_now = True, verbose_name = 'Дата/время изменения' )

	@property
	def wiki_data_url( self ):
		return f'https://www.wikidata.org/wiki/{self.wiki_data_id}'

	@property
	def population_density( self ):
		return self.population / self.area if self.area else 0

	@property
	def part_world( self ):
		return self.region_world.part_world

	def __str__(self):
		return self.name_ru

	class Meta:
		verbose_name = 'страна'
		verbose_name_plural = '2. Страны мира'
		db_table = 'geo_countries'
		ordering = ['id']


class GeoNodeType( m.Model ):
	name_en = m.CharField( max_length = 80, db_index = True, unique = True, verbose_name = 'Тип узла ENG' )
	name_ru = m.CharField( max_length = 80, blank = True, null = True, verbose_name = 'Тип узла RUS' )

	description_en = m.CharField( max_length = 250, blank = True, null = True, verbose_name = 'Описание типа узла ENG' )
	description_ru = m.CharField( max_length = 250, blank = True, null = True, verbose_name = 'Описание типа узла RUS' )

	def __str__( self ):
		return f'Geo node type {self.name_en}'

	class Meta:
		verbose_name = 'тип гео-узла'
		verbose_name_plural = 'типы гео-узлов'
		db_table = 'geo_nodes_types'
		ordering = ['id']


class GeoNode( m.Model ):
	"""Федеральный округ / макрорегион / регион / область / и т.д."""
	country   = m.ForeignKey( GeoCountry, on_delete = m.CASCADE, related_name = 'nodes', verbose_name = 'Страна' )
	node_type = m.ForeignKey( GeoNodeType, on_delete = m.CASCADE, related_name = 'nodes', verbose_name = 'Тип узла' )

	parent = m.ForeignKey( 'self', on_delete = m.CASCADE, related_name = 'children',
	                       blank = True, null = True, verbose_name = 'Родитель' )
	level  = m.PositiveSmallIntegerField( blank = True,null = True, verbose_name = 'Уровень' )

	name_ru     = m.CharField( max_length = 250, db_index = True, verbose_name = 'Название RUS' )
	name_en     = m.CharField( max_length = 250, verbose_name = 'Название ENG' )
	name_native = m.CharField( max_length = 250, verbose_name = 'Родное название' )

	latitude = m.FloatField(
		verbose_name = 'Широта центра', blank = True, null = True,
		validators = [MinValueValidator( -90.0 ), MaxValueValidator( 90.0 )]
	)
	longitude = m.FloatField(
		verbose_name = 'Долгота центра', blank = True, null = True,
		validators = [MinValueValidator( -180.0 ), MaxValueValidator( 180.0 )]
	)

	timezone     = m.ForeignKey( 'TimeZone', on_delete = m.CASCADE, verbose_name = 'Часовой пояс' )
	population   = m.BigIntegerField( null = True, blank = True, verbose_name = 'Население' )
	iso_code     = m.CharField( max_length = 20, blank = True, null = True, verbose_name = 'ICO 3166-2' )
	wiki_data_id = m.CharField( max_length = 30, blank = True, null = True, verbose_name = 'Wikipedia ID' )

	created_at = m.DateTimeField( db_index = True, verbose_name = 'Добавлено' )
	updated_at = m.DateTimeField( db_index = True, verbose_name = 'Обновлено' )

	@property
	def full_path( self ):
		"""Полный путь: Страна > Округ > Регион > ..."""
		path = [self.name_ru]
		node = self

		while node.parent:
			node = node.parent
			path.insert( 0, node.name_ru )

		path.insert( 0, self.country.name_ru )

		return " > ".join( path )

	@property
	def name_with_type( self ):
		if not self.node_type:
			return self.name_native
		return f'{self.node_type.name_ru} {self.name_native}'

	@property
	def wiki_data_url( self ):
		if not self.wiki_data_id:
			return None
		return f'https://www.wikidata.org/wiki/{self.wiki_data_id}'

	def __str__(self):
		return f'{self.country.name_ru} - {self.name_ru}'

	class Meta:
		verbose_name = 'гео-узел'
		verbose_name_plural = '3. Гео-узлы'
		db_table = 'geo_nodes'
		ordering = ['country', 'name_ru']


class GeoCity( m.Model ):
	"""Город"""
	node   = m.ForeignKey( GeoNode, on_delete = m.CASCADE, db_index = True,
		                   related_name = 'cities', verbose_name = 'Регион' )

	name_ru = m.CharField( max_length = 250, db_index = True, verbose_name = 'Название RUS' )
	name_en = m.CharField( max_length = 250, verbose_name = 'Название ENG' )
	name_native = m.CharField( max_length = 250, verbose_name = 'Родное название' )

	latitude   = m.FloatField(
		verbose_name = 'Широта',
		validators = [MinValueValidator( -90.0 ), MaxValueValidator( 90.0 )]
	)
	longitude  = m.FloatField(
		verbose_name = 'Долгота',
		validators = [MinValueValidator( -180.0 ), MaxValueValidator( 180.0 )]
	)

	timezone     = m.ForeignKey( 'TimeZone', on_delete = m.CASCADE, verbose_name = 'Часовой пояс' )
	population   = m.BigIntegerField( null = True, blank = True, verbose_name = 'Население' )
	wiki_data_id = m.CharField( max_length = 30, blank = True, null = True, verbose_name = 'Wikipedia ID' )

	created_at = m.DateTimeField( db_index = True, verbose_name = 'Дата/время записи' )
	updated_at = m.DateTimeField( verbose_name = 'Дата/время изменения' )

	@property
	def full_path( self ):
		"""Полный путь: Страна > Округ > Регион > ... > Город"""
		path = [self.name_ru]

		path.insert( 0, self.node.name_ru )

		while self.node.parent:
			node = self.node.parent
			path.insert( 0, node.name_ru )

		path.insert( 0, self.node.country.name_ru )

		return " > ".join( path )

	@property
	def wiki_data_url( self ):
		if not self.wiki_data_id:
			return None
		return f'https://www.wikidata.org/wiki/{self.wiki_data_id}'

	def __str__(self):
		return f'{self.name_ru}, {self.node.name_ru}'

	class Meta:
		verbose_name = 'город'
		verbose_name_plural = '4. Города'
		db_table = 'geo_cities'
		ordering = ['node', 'name_ru']


class GeoStreetType( m.Model ):
	"""Тип улицы"""
	short_ru = m.CharField( max_length = 10, db_index = True, verbose_name = 'Тип ( краткий | RUS )' )
	short_en = m.CharField( max_length = 10, db_index = True, verbose_name = 'Тип ( краткий | ENG )' )

	long_ru = m.CharField( max_length = 30, verbose_name = 'Тип ( полный | RUS )' )
	long_en = m.CharField( max_length = 30, verbose_name = 'Тип ( полный | ENG )' )

	variants_ru = m.JSONField( default = list, db_index = True, verbose_name = 'Варианты ( RUS )',
	                           help_text = '["ул.", "ул", "улица", "улице", "улицы"]' )
	variants_en = m.JSONField( default = list, db_index = True, verbose_name = 'Варианты ( RUS )',
	                           help_text = '["St.", "St", "street", "str.", "ul."]' )

	order  = m.PositiveSmallIntegerField( default = 0, verbose_name = 'Порядок сортировки',
	                                      help_text = 'Порядок сортировки в выпадающем списке' )

	def __str__(self):
		return f'{self.short_ru} | {self.long_ru}'

	class Meta:
		verbose_name = 'тип улицы'
		verbose_name_plural = 'типы улиц'
		db_table = 'geo_streets_types'
		ordering = ['order']


class GeoStreet( m.Model ):
	"""Улица"""
	city        = m.ForeignKey( GeoCity, on_delete = m.CASCADE, related_name = 'streets', verbose_name = 'Город' )
	street_type = m.ForeignKey( GeoStreetType, on_delete = m.PROTECT, related_name = 'streets', verbose_name = 'Тип улицы' )

	name_native = m.CharField( max_length = 250, verbose_name = 'Название' )
	name_lower = m.CharField( max_length = 250, db_index = True, editable = False )

	created_at  = m.DateTimeField( auto_now_add = True, db_index = True, verbose_name = 'Дата/время записи' )
	updated_at  = m.DateTimeField( auto_now = True, verbose_name = 'Дата/время изменения' )

	@property
	def name_with_type( self ):
		if not self.name_native or not self.street_type:
			return None
		return f'{self.street_type.short_ru} {self.name_native}'

	def save( self, *args, **kwargs ):
		# Автоматически заполняем поле для поиска
		self.name_lower = self.name_native.lower()
		super().save( *args, **kwargs )

	def __str__(self):
		return f'{self.street_type.short_ru} {self.name_native}, {self.city.name_ru}'

	class Meta:
		verbose_name = 'улица'
		verbose_name_plural = '5. Улицы'
		db_table = 'geo_streets'
		ordering = ['city', 'street_type', 'name_native']
		unique_together = [
			('city', 'street_type', 'name_native'),  # Исключаем дубли
			('city', 'name_lower'),  # Исключаем разный регистр
		]
