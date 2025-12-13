from django.contrib import admin
from django.db.models import Count
from django.utils.safestring import mark_safe

from geodata.models import (
	GeoPartWorld,
	GeoRegionWorld,
	GeoCountry,
	GeoNodeType,
	GeoNode,
	GeoCity,
	GeoStreetType,
	GeoStreet,
)


class GeoRegionWorldInline( admin.TabularInline  ):
	model = GeoRegionWorld
	extra = 0
	fields = [ 'name_ru', 'name_en' ]
	readonly_fields = [ 'name_ru', 'name_en' ]
	show_change_link = True
	can_delete = False
	can_add = False

@admin.register(GeoPartWorld)
class GeoPartWorldAdmin(admin.ModelAdmin):
	list_display  = [ 'id', 'name_ru', 'name_en', 'regions_count' ]
	search_fields = [ 'name_ru', 'name_en' ]
	readonly_fields = [ 'wiki_data_id', 'wiki_data_url' ]
	ordering = ['id']

	inlines = [GeoRegionWorldInline]

	def regions_count( self, obj ):
		return obj.regions_world.count()

	regions_count.short_description = "Регионов"


class GeoCountryInline( admin.TabularInline  ):
	model = GeoCountry
	extra = 0
	fields = [ 'cca3', 'name_ru', 'name_en', 'name_official_ru', 'name_official_en',
	           'capital_ru', 'capital_en', 'area', 'population' ]
	readonly_fields = [ 'cca3', 'name_ru', 'name_en', 'name_official_ru', 'name_official_en',
	                    'capital_ru', 'capital_en', 'area', 'population' ]
	show_change_link = True
	can_delete = False
	can_add = False

@admin.register(GeoRegionWorld)
class GeoRegionWorldAdmin(admin.ModelAdmin):
	list_display  = [ 'id', 'name_ru', 'name_en', 'counties_count' ]
	search_fields = [ 'name_ru', 'name_en' ]
	readonly_fields = [ 'wiki_data_id', 'wiki_data_url' ]
	list_select_related = [ 'part_world' ]
	ordering = ['id']

	inlines = [GeoCountryInline]

	def counties_count( self, obj ):
		return obj.countries.count()

	counties_count.short_description = "Стран"


@admin.register(GeoCountry)
class GeoCountryAdmin(admin.ModelAdmin):
	list_display = [
		'get_flag', 'name_ru', 'name_official_ru', 'region_world', 'capital_ru',
		'is_member_oon'
	]
	list_filter = [
		'region_world', 'is_independent', 'is_member_oon', 'is_landlocked',
		'is_handly_verify'
	]
	search_fields = [
		'name_ru', 'name_official_ru', 'capital_ru', 'cca2', 'cca3', 'ccn3'
	]
	readonly_fields = [
		'wiki_data_id', 'wiki_data_url', 'population_density', 'get_flag',
		'datetime_create', 'datetime_edit'
	]
	list_select_related = [ 'region_world' ]
	ordering = [ 'name_ru' ]
	list_per_page = 250

	fieldsets = (
		( 'География', {
			'fields': (
				'region_world',
				( 'name_ru', 'name_official_ru' ),
				( 'name_en', 'name_official_en' ),
				( 'capital_ru', 'capital_en' )
			)
		}),
		( 'Обозначения и коды', {
			'fields': (
				( 'cca2', 'cca3', 'ccn3' ),
				( 'currency_code', 'currency_name', 'currency_symbol' ),
				( 'phone_code', 'top_level_domain' )
			)
		}),
		( 'Флаг', {
			'fields': (
				('emoji_code', 'emoji_flag'),
				'flag',
				'get_flag'
			)
		}),
		( 'Геоданные', {
			'fields': (
				'area',
				'population',
				'population_density',
				'latitude',
				'longitude'
			)
		}),
		( 'Чекбоксы', {
			'fields': (
				'is_landlocked',
				'is_independent',
				'is_member_oon',
				'is_handly_verify'
			)
		}),
		( 'Wiki', {
			'fields': (
				'wiki_data_id',
				'wiki_data_url'
			)
		}),
		( 'Временные метки', {
			'fields': (
				'datetime_create',
				'datetime_edit'
			)
		}),
	)

	def get_flag( self, obj ):
		if obj.flag:
			return mark_safe( f'<img src="{obj.flag.url}" width="100" />' )
		else:
			return 'Ещё нет'

	get_flag.short_description = 'Флаг'


@admin.register( GeoNodeType )
class GeoNodeTypeAdmin( admin.ModelAdmin ):
	list_display = [ 'name_ru', 'description_ru' ]
	ordering     = [ 'name_ru' ]
	list_per_page = 101


@admin.register( GeoNode )
class GeoNodeAdmin( admin.ModelAdmin ):
	list_display = [
		'name_ru', 'node_type__name_ru', 'country', 'iso_code',
		'timezone__tz', 'level'
	]
	list_filter = [ 'country']
	search_fields = [ 'name_ru', 'country__name_ru', 'name_en', 'name_native' ]
	list_select_related = [ 'country' ]
	readonly_fields = [
		'parent', 'level', 'full_path', 'latitude', 'longitude',
		'wiki_data_id', 'wiki_data_url', 'created_at', 'updated_at'
	]
	ordering = [ 'country__name_ru', 'name_ru' ]
	list_per_page = 250

	fieldsets = (
		( 'География', {
			'fields': (
				'country',
				'node_type',
				( 'parent', 'level' ),
				'full_path'
			)
		}),
		( 'Название', {
			'fields': (
				'name_ru',
				'name_en',
				'name_native',
			)
		}),
		( 'Инфо', {
			'fields': (
				'iso_code',
				'timezone',
				'population',
			)
		}),
		( 'Расположение', {
			'fields': (
				'latitude',
				'longitude',
			)
		}),
		( 'Wiki', {
			'fields': (
				'wiki_data_id',
				'wiki_data_url'
			)
		}),
		( 'Временные метки', {
			'fields': (
				'created_at',
				'updated_at'
			)
		}),

	)


@admin.register(GeoCity)
class GeoCityAdmin(admin.ModelAdmin):
	list_display = [
		'name_ru', 'full_path'
	]
	list_filter = [
		'node__country'
	]
	search_fields = ['name_ru']
	readonly_fields = [ 'full_path', 'created_at', 'updated_at']
	list_select_related = ['node', 'node__country']
	ordering = ['node__country__name_ru', 'node__name_ru', 'name_ru']
	autocomplete_fields = ['node']
	list_per_page = 250

	@admin.display(description='Округ')
	def district(self, obj):
		return obj.node

	@admin.display(description='Страна')
	def country(self, obj):
		return obj.node.country


@admin.register( GeoStreetType )
class GeoStreetTypeAdmin( admin.ModelAdmin ):
	list_display = [
		'short_ru', 'long_ru', 'variants_ru', 'streets_count', 'order'
	]
	ordering = [ 'order' ]

	fieldsets = (
		( 'Русский', {
			'fields': (
				'short_ru',
				'long_ru',
				'variants_ru'
			)
		}),
		( 'English', {
			'fields': (
				'short_en',
				'long_en',
				'variants_en'
			)
		}),
		( 'Порядок', {
			'fields': (
				'order',
			)
		}),
	)

	def get_queryset( self, request ):
		qs = super().get_queryset( request )
		return qs.annotate( streets_count = Count( 'streets' ) )

	def streets_count( self, obj ):
		return obj.streets_count

	streets_count.short_description = 'Кол-во улиц'


@admin.register( GeoStreet )
class GeoStreetAdmin( admin.ModelAdmin ):
	list_display = [ 'name_with_type', 'city', 'created_at' ]
	list_filter  = [ 'street_type' ]
	autocomplete_fields = [ 'city' ]
	readonly_fields = [ 'name_with_type', 'created_at', 'updated_at' ]
	search_fields = [ 'name_native', 'city__name_ru' ]
	ordering = [ 'city', 'street_type', 'name_native' ]

	fieldsets = (
		( 'Основное', {
			'fields': (
				'city',
				'name_with_type',
				( 'street_type', 'name_native' ),
			)
		}),
		( 'Временные метки', {
			'fields': (
				'created_at',
				'updated_at'
			)
		}),
	)
