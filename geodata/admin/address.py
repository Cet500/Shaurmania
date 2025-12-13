from django.contrib import admin

from geodata.models import BaseAddress, Address


@admin.register( BaseAddress )
class BaseAddressAdmin(admin.ModelAdmin):
	list_display = [ 'full_address', 'normal_address', 'created_at' ]
	list_filter = [ 'created_at' ]
	autocomplete_fields = [ 'street' ]
	search_fields = [ 'street', 'full_address' ]
	readonly_fields = [ 'latitude', 'longitude', 'full_address', 'normal_address', 'updated_at', 'created_at' ]
	list_per_page = 250

	fieldsets = (
		( 'Улица и дом', {
			'fields': (
				'street',
				( 'house', 'building' ),
				'postal_code',
				'is_verified'
			)
		}),
		( 'Полный адрес', {
			'fields': (
				'full_address',
				'normal_address'
			)
		}),
		( 'Геоданные', {
			'fields': (
				'latitude',
				'longitude'
			)
		}),
		( 'Временные метки', {
			'fields': (
				'updated_at',
				'created_at'
			)
		}),
	)


@admin.register(Address)
class AddressAdmin( admin.ModelAdmin ):
	list_display = [ 'full_address', 'created_at' ]
	list_filter = [ 'created_at' ]
	autocomplete_fields = [ 'base' ]
	search_fields = [ 'base__full_address' ]
	readonly_fields = [ 'normal_address', 'full_address', 'updated_at', 'created_at' ]
	list_per_page = 250

	fieldsets = (
		( 'Основное', {
			'fields': (
				'base',
				'entrance',
				'floor',
				( 'apartment', 'intercom' )
			)
		}),
		( 'Полный адрес', {
			'fields': (
				'full_address',
				'normal_address'
			)
		}),
		( 'Временные метки', {
			'fields': (
				'created_at',
				'updated_at'
			)
		}),
	)
