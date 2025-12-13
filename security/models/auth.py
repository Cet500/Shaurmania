from uuid import uuid4
from datetime import datetime

from django.db import models as m
from uaparser import UAParser

from geodata.models import GeoCountry
from main.models import User


class SecurityDevice( m.Model ):
	uuid = m.UUIDField( primary_key = True, default = uuid4, unique = True, db_index = True, editable = False,
						verbose_name = 'UUID устройства' )

	user_agent_full = m.CharField( max_length = 255, null = True, verbose_name = 'Полный User-Agent' )
	browser_name    = m.CharField( max_length = 40,  null = True, verbose_name = 'Браузер / имя' )
	browser_version = m.CharField( max_length = 40,  null = True, verbose_name = 'Браузер / версия полная' )
	browser_major   = m.CharField( max_length = 10,  null = True, verbose_name = 'Браузер / версия' )
	device_vendor   = m.CharField( max_length = 40,  null = True, verbose_name = 'Устройство / производитель' )
	device_model    = m.CharField( max_length = 40,  null = True, verbose_name = 'Устройство / модель' )
	device_type     = m.CharField( max_length = 20,  null = True, verbose_name = 'Устройство / тип' )
	engine_name     = m.CharField( max_length = 20,  null = True, verbose_name = 'Движок / имя' )
	engine_version  = m.CharField( max_length = 20,  null = True, verbose_name = 'Движок / версия' )
	os_name         = m.CharField( max_length = 40,  null = True, verbose_name = 'ОС / Имя' )
	os_version      = m.CharField( max_length = 20,  null = True, verbose_name = 'ОС / Версия' )
	cpu             = m.CharField( max_length = 20,  null = True, verbose_name = 'Процессор' )

	created_at = m.DateTimeField( auto_now_add = True, verbose_name = 'Время создания' )

	@staticmethod
	def from_user_agent( user_agent_str ):
		ua = UAParser.parse( user_agent_str )

		return SecurityDevice(
			user_agent_full = user_agent_str,
			browser_name    = ua.browser.family,
			browser_version = ua.browser.version_string,
			browser_major   = ua.browser.major,
			device_vendor   = ua.device.brand,
			device_model    = ua.device.model,
			device_type     = ua.device.family,
			engine_name     = ua.engine.family,
			engine_version  = ua.engine.version_string,
			os_name         = ua.os.family,
			os_version      = ua.os.version_string,
			cpu             = ua.device.cpu,
		)

	def __str__( self ):
		return f'{self.browser_name} {self.browser_version} на {self.device_model}'

	class Meta:
		verbose_name = 'устройство'
		verbose_name_plural = 'устройства'
		db_table = 'security_device'


class SecurityAuthLog( m.Model ):
	user       = m.ForeignKey( User, on_delete = m.CASCADE, db_index = True,
							   related_name = 'security_logs', verbose_name = 'Пользователь' )
	device     = m.ForeignKey( SecurityDevice, on_delete = m.CASCADE, db_index = True,
							   related_name = 'auths', verbose_name = 'Устройство' )

	ip_country = m.ForeignKey( GeoCountry, on_delete = m.SET_NULL, null = True, blank = True,
							   verbose_name = 'Страна по IP' )
	ip_address = m.GenericIPAddressField( protocol = 'IPv4', verbose_name = 'IP входа' )

	is_success = m.BooleanField( default = True, db_index = True, verbose_name = 'Успешность входа' )

	login_at   = m.DateTimeField( auto_now_add = True, db_index = True, verbose_name = 'Время входа' )
	logout_at  = m.DateTimeField( default = None, blank = True, verbose_name = 'Время выхода' )

	@property
	def online_time( self ):
		if self.logout_at:
			return self.logout_at - self.login_at
		else:
			return datetime.now() - self.login_at

	def save( self, *args, **kwargs ):
		# if self.ip_address:

		super().save( *args, **kwargs )

	def __str__( self ):
		return f'{self.user.username} вошёл {self.login_at:%d.%m.%Y %H:%M} с {self.ip_address}'

	class Meta:
		verbose_name = 'лог авторизации'
		verbose_name_plural = 'логи авторизации'
		db_table = 'security_auth_log'
		ordering = [ '-login_at' ]
