from django.db import models as m

from main.models import User


ACTION_VALUES = {
	1: 'Мусорное',
	2: 'Неважное',
	3: 'Обычное',
	4: 'Важное',
	5: 'Критическое',
}

class SecurityAction( m.Model ):
	action_code  = m.CharField( max_length = 20, unique = True, verbose_name = 'Код действия' )
	action_name  = m.CharField( max_length = 30, verbose_name = 'Название действия' )
	template     = m.CharField( max_length = 250, verbose_name = 'Шаблон уведомления' )
	action_value = m.SmallIntegerField( default = 3, choices = ACTION_VALUES, verbose_name = 'Сила важности уведомления' )

	def __str__( self ):
		return self.action_code

	class Meta:
		verbose_name = 'тип уведомления безопасности'
		verbose_name_plural = 'типы уведомлений безопасности'
		db_table = 'security_action'


class SecurityNotice( m.Model ):
	user      = m.ForeignKey( User, on_delete = m.CASCADE, db_index = True,
							  related_name = 'security_notices', verbose_name = 'Пользователь' )
	action    = m.ForeignKey( SecurityAction, on_delete = m.PROTECT, verbose_name = 'Действие' )

	is_read   = m.BooleanField( default = False, verbose_name = 'Прочитано' )
	channel   = m.CharField( max_length = 20, default = 'website', verbose_name = 'Канал отправки' )

	notice_at = m.DateTimeField( auto_now_add = True, verbose_name = 'Время уведомления' )

	def __str__( self ):
		return f"{self.user.username} — {self.action.action_code} в {self.notice_at:%d.%m.%Y %H:%M}"

	class Meta:
		verbose_name = 'уведомление безопасности'
		verbose_name_plural = 'уведомления безопасности'
		db_table = 'security_notice'
		ordering = ['-notice_at']
