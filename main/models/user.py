from django.db import models as m
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager( BaseUserManager ):
	def create_user( self, email, username, password, **extra_fields ):
		if not username:
			raise ValueError( 'Введите имя пользователя' )

		if not email:
			raise ValueError( 'Это не Email' )

		email = self.normalize_email( email )
		user = self.model( email = email, username = username, **extra_fields )

		user.set_password( password )
		user.save()

		return user

	def create_superuser( self, username, email, password, **extra_fields ):
		extra_fields.setdefault( 'is_staff', True )
		extra_fields.setdefault( 'is_superuser', True )

		return self.create_user( email, username, password, **extra_fields )


class User( AbstractBaseUser, PermissionsMixin ):
	username     = m.CharField( max_length = 60, unique = True, verbose_name = 'Никнейм' )
	picture      = m.ImageField( upload_to = 'user_images', verbose_name = 'Изображение' )
	email        = m.EmailField( max_length = 80, verbose_name = 'Email' )
	number       = m.CharField( max_length = 17, verbose_name = 'Номер' )
	last_address = m.CharField( max_length = 200, verbose_name = 'Адрес последней доставки' )
	reg_date     = m.DateTimeField( auto_now_add = True, verbose_name = 'время регистрации' )

	is_open   = m.BooleanField( default = True, verbose_name = 'Открытый профиль?' )
	is_active = m.BooleanField( default = True, verbose_name = 'Профиль активен?' )
	is_staff  = m.BooleanField( default = False, verbose_name = 'Это сотрудник сайта?' )

	objects = UserManager()

	USERNAME_FIELD = 'username'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = ['email']

	def __str__( self ):
		return f'{self.username} | {self.email}'

	class Meta:
		verbose_name = 'пользователь'
		verbose_name_plural = 'пользователи'
		ordering = ['username']
