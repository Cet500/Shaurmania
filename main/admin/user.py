from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from main.models import User, UserAchievement


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
				'avatar',
				# 'get_avatar_256',
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
		if obj.avatar:
			return mark_safe( f'<img src="{obj.avatar_32x.url}" width="32" />' )
		else:
			return mark_safe( f'<b>нет</b>' )

	get_avatar_32.short_description = 'Aва'

	def get_avatar_256( self, obj ):
		if obj.avatar:
			return mark_safe( f'<img src="{obj.avatar_256x.url}" width="256" />' )
		else:
			return mark_safe( f'<b>нет</b>' )

	get_avatar_256.short_description = 'Аватар 256x'

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
