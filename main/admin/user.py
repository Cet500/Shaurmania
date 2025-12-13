from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from main.models import (
	User,
	UserAchievement,
	UserAvatar,
	UserSocialLink,
	UserAddress,
)


@admin.register( User )
class UserAdmin( BaseUserAdmin ):
	# Настройка списка объектов
	list_display = [
		'get_avatar_32', 'username', 'email', 'name', 'lastname', 'phone',
		'is_active', 'is_staff', 'register_at'
	]
	list_filter = [
		'is_active', 'is_staff', 'is_superuser', 'is_open',
		'sex', 'main_lang', 'register_at'
	]
	list_display_links = [ 'username' ]
	search_fields = [
		'username', 'email', 'name', 'lastname', 'patronymic', 'phone'
	]
	readonly_fields = [
		'id', 'password', 'register_at', 'updated_at', 'last_login'
	]
	filter_horizontal = [ 'groups', 'user_permissions' ]
	ordering = [ '-register_at' ]
	list_per_page = 100

	# Группировка полей в форме редактирования
	fieldsets = (
		( 'Учетные данные', {
			'fields': (
				'username',
				'password',
				( 'email', 'email_status' ),
				( 'phone', 'phone_status' )
			)
		}),
		( 'Персональная информация', {
			'fields': (
				('name', 'lastname', 'patronymic'),
				'date_of_birth',
				'sex',
				'description',
				'last_address'
			)
		}),
		( 'Настройки', {
			'fields': (
				'main_lang',
				'is_open'
			)
		}),
		( 'Права и группы', {
			'fields' : (
				'is_active',
				'is_staff',
				'is_superuser',
				'groups',
				'user_permissions',
			),
			'classes': ('collapse', )  # свернем, так как эти поля не часто меняются
		}),
		( 'Временные метки', {
			'fields' : (
				'last_login', 'register_at', 'updated_at',
			)
		}),
	)

	def get_avatar_32( self, obj ):
		return mark_safe( f'<img src="{obj.avatar_48_url}" width="48" style="border-radius: 24px;" />' )

	get_avatar_32.short_description = 'Aва'

	def has_add_permission(self, request):
		"""Запрет на добавление"""
		return request.user.is_superuser

	def has_change_permission( self, request, obj = None ):
		"""Проверка прав на изменение"""
		if not request.user.is_staff:
			return False

		if obj and obj.is_superuser and not request.user.is_superuser:
			return False

		return super().has_change_permission( request, obj )

	def has_delete_permission( self, request, obj = None ):
		"""Проверка прав на удаление"""
		if not request.user.is_staff:
			return False

		if obj and obj.is_superuser:
			return False

		if obj and obj == request.user:
			return False

		return super().has_delete_permission( request, obj )

	def get_queryset( self, request ):
		"""Ограничение видимости пользователей для не-суперпользователей"""
		qs = super().get_queryset( request )
		if not request.user.is_superuser:
			# Обычные staff видят только не-суперпользователей
			qs = qs.filter( is_superuser = False )
		return qs


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
	list_display = [ 'user', 'achievement', 'get_date' ]
	list_filter  = [ 'get_date' ]


@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
	list_display = ['user', 'is_primary', 'uploaded_at', 'avatar_preview']
	list_filter = ['is_primary', 'uploaded_at']
	search_fields = ['user__username', 'user__email']
	readonly_fields = ['uploaded_at', 'avatar_preview']
	list_select_related = ['user']

	def avatar_preview(self, obj):
		if obj.avatar:
			return mark_safe(f'<img src="{obj.avatar.url}" width="64" style="border-radius: 8px;" />')
		return '—'

	avatar_preview.short_description = 'Превью'


@admin.register(UserSocialLink)
class UserSocialLinkAdmin(admin.ModelAdmin):
	list_display = [
		'user', 'network', 'link', 'is_verified',
		'is_primary', 'is_shown', 'created_at'
	]
	list_filter = ['network', 'is_verified', 'is_primary', 'is_shown', 'created_at']
	search_fields = ['user__username', 'user__email', 'link', 'description']
	readonly_fields = ['created_at', 'updated_at']
	list_select_related = ['user']


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
	list_display = [
		'user', 'address', 'is_default', 'updated_at'
	]
	list_filter = [ 'is_default' ]
	search_fields = [
		'user__username', 'user__email'
	]
	readonly_fields = [ 'created_at', 'updated_at' ]
	autocomplete_fields = [ 'user', 'address' ]
	list_select_related = [ 'user', 'address' ]

	fieldsets = (
		( 'Адрес', {
			'fields': (
				'user',
				'address'
			)
		}),
		( 'Детали адреса', {
			'fields': (
				'title',
				'notes',
				'is_default'
			)
		}),
		( 'Системные', {
			'fields' : (
				'created_at',
				'updated_at'
			),
		}),
	)
