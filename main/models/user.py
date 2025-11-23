from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, EmailValidator
from django.db import models as m
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField

from Shaurmania.settings import MIN_AGE_REGISTRATION, MAX_AGE_REGISTRATION


class UserManager( BaseUserManager ):
	def create_user( self, name, email, username, password, **extra_fields ):
		if not name:
			raise ValueError( 'Введите имя' )

		if not username:
			raise ValueError( 'Введите логин' )

		if not email:
			raise ValueError( 'Введите Email' )

		email = self.normalize_email( email )
		user = self.model( name = name, email = email, username = username, **extra_fields )

		user.set_password( password )
		user.save()

		return user

	def create_superuser( self, name, username, email, password, **extra_fields ):
		extra_fields.setdefault( 'is_staff', True )
		extra_fields.setdefault( 'is_superuser', True )

		return self.create_user( name, email, username, password, **extra_fields )


SEX = {
	'M': 'Male', 'F': 'Female', 'O': 'Other', 'N': 'Null'
}
LANGS = {
	'RU': 'Русский', 'EN': 'English'
}
VERIFY_STATUSES = {
	'N': 'None', 'V': 'Verified', 'R': 'Reality Verified'
}

def validate_age(value):
	today = date.today()
	min_age = today.replace( year = today.year - MIN_AGE_REGISTRATION )  # Минимум лет
	max_age = today.replace( year = today.year - MAX_AGE_REGISTRATION )  # Максимум лет

	if value > min_age:
		raise ValidationError(f'Возраст должен быть не менее {MIN_AGE_REGISTRATION} лет.')
	if value < max_age:
		raise ValidationError(f'Возраст не может превышать {MAX_AGE_REGISTRATION} лет.')


class User( AbstractBaseUser, PermissionsMixin ):
	name         = m.CharField( max_length = 40, verbose_name = 'Имя' )
	lastname     = m.CharField( max_length = 40, blank = True, null = True, verbose_name = 'Фамилия' )
	patronymic   = m.CharField( max_length = 40, blank = True, null = True, verbose_name = 'Отчество' )

	description  = m.CharField( max_length = 240, blank = True, verbose_name = 'Описание' )
	last_address = m.CharField( max_length = 200, blank = True, verbose_name = 'Адрес последней доставки' )

	sex          = m.CharField( max_length = 1, default = 'N', choices = SEX, verbose_name = 'Пол' )
	main_lang    = m.CharField( max_length = 2, default = 'RU', choices = LANGS, verbose_name = 'Язык' )

	username     = m.CharField( max_length = 60, unique = True, db_index = True, verbose_name = 'Никнейм' )
	email        = m.EmailField(
		validators = [ EmailValidator ], max_length = 80, unique = True, db_index = True, verbose_name = 'Email'
	)
	email_status = m.CharField(
		max_length = 1, default = 'N', choices = VERIFY_STATUSES, verbose_name = 'Статус email'
	)

	phone        = PhoneNumberField( unique = True, null = False, blank = False, verbose_name = 'Телефон' )
	phone_status = m.CharField(
		max_length = 1, default = 'N', choices = VERIFY_STATUSES, verbose_name = 'Статус телефона'
	)

	date_of_birth = m.DateField(
		null = True, blank = True, validators = [ validate_age ], verbose_name = 'Дата рождения'
	)

	avatar       = m.ImageField(
		upload_to = 'user_avatars', verbose_name = 'Аватар', null = True, blank = True,
		validators = [ FileExtensionValidator( ['jpg', 'jpeg', 'png', 'webp'] ) ]
	)
	avatar_32x   = ImageSpecField(
		source = 'avatar',
		processors = [ResizeToFill( 32, 32 )],
		format = 'PNG',
		options = { 'quality': 100 },
	)
	avatar_48x = ImageSpecField(
		source = 'avatar',
		processors = [ResizeToFill( 48, 48 )],
		format = 'PNG',
		options = { 'quality': 100 },
	)
	avatar_64x = ImageSpecField(
		source = 'avatar',
		processors = [ResizeToFill( 64, 64 )],
		format = 'PNG',
		options = { 'quality': 100 },
	)
	avatar_128x = ImageSpecField(
		source = 'avatar',
		processors = [ResizeToFill( 128, 128 )],
		format = 'PNG',
		options = { 'quality': 90 },
	)
	avatar_256x = ImageSpecField(
		source = 'avatar',
		processors = [ResizeToFill( 256, 256 )],
		format = 'PNG',
		options = { 'quality': 90 },
	)

	register_at  = m.DateTimeField( auto_now_add = True, verbose_name = 'Время регистрации' )
	updated_at   = m.DateTimeField( auto_now = True, verbose_name = "Время обновления" )

	is_open   = m.BooleanField( default = True, verbose_name = 'Открытый профиль?' )
	is_active = m.BooleanField( default = True, verbose_name = 'Профиль активен?' )
	is_staff  = m.BooleanField( default = False, verbose_name = 'Это сотрудник сайта?' )

	objects = UserManager()

	USERNAME_FIELD = 'username'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'email']

	def save( self, *args, **kwargs ):
		if self.avatar:
			self.avatar_32x.generate()
			self.avatar_48x.generate()
			self.avatar_64x.generate()
			self.avatar_128x.generate()
			self.avatar_256x.generate()

		super().save( *args, **kwargs )

	def __str__( self ):
		return f'{self.username} | {self.email}'

	class Meta:
		verbose_name = 'пользователь'
		verbose_name_plural = 'пользователи'
		ordering = ['username']
