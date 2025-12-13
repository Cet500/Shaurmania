from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, EmailValidator, URLValidator
from django.db import models as m
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.templatetags.static import static
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from phonenumber_field.modelfields import PhoneNumberField

from geodata.models import Address
from main.validators import validate_not_in_stop_words, validate_social_link
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

	if value < min_age:
		raise ValidationError(f'Возраст должен быть не менее {MIN_AGE_REGISTRATION} лет.')
	if value > max_age:
		raise ValidationError(f'Возраст не может превышать {MAX_AGE_REGISTRATION} лет.')


class User( AbstractBaseUser, PermissionsMixin ):
	name         = m.CharField( max_length = 40,
	                            validators = [ validate_not_in_stop_words ], verbose_name = 'Имя' )
	lastname     = m.CharField( max_length = 40, blank = True, null = True,
	                            validators = [ validate_not_in_stop_words ], verbose_name = 'Фамилия' )
	patronymic   = m.CharField( max_length = 40, blank = True, null = True,
	                            validators = [ validate_not_in_stop_words ], verbose_name = 'Отчество' )

	description  = m.CharField( max_length = 240, blank = True, verbose_name = 'Описание' )
	last_address = m.CharField( max_length = 200, blank = True, verbose_name = 'Адрес последней доставки' )

	sex          = m.CharField( max_length = 1, default = 'N', choices = SEX, verbose_name = 'Пол' )
	main_lang    = m.CharField( max_length = 2, default = 'RU', choices = LANGS, verbose_name = 'Язык' )

	username     = m.CharField( max_length = 60, unique = True, db_index = True,
	                            validators = [ validate_not_in_stop_words ], verbose_name = 'Никнейм' )
	email        = m.EmailField(
		validators = [ EmailValidator ], max_length = 80, unique = True, db_index = True, verbose_name = 'Email'
	)
	email_status = m.CharField(
		max_length = 1, default = 'N', choices = VERIFY_STATUSES, verbose_name = 'Статус email'
	)

	phone        = PhoneNumberField( unique = True, null = True, blank = True, db_index=True, verbose_name = 'Телефон' )
	phone_status = m.CharField(
		max_length = 1, default = 'N', choices = VERIFY_STATUSES, verbose_name = 'Статус телефона'
	)

	date_of_birth = m.DateField(
		null = True, blank = True, validators = [ validate_age ], verbose_name = 'Дата рождения'
	)

	register_at  = m.DateTimeField( auto_now_add = True, db_index = True, verbose_name = 'Время регистрации' )
	updated_at   = m.DateTimeField( auto_now = True, verbose_name = "Время обновления" )

	is_open   = m.BooleanField( default = True,  db_index = True, verbose_name = 'Открытый профиль?' )
	is_active = m.BooleanField( default = True,  db_index = True, verbose_name = 'Профиль активен?' )
	is_staff  = m.BooleanField( default = False, db_index = True, verbose_name = 'Это сотрудник сайта?' )

	objects = UserManager()

	USERNAME_FIELD = 'username'
	EMAIL_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'email']

	@property
	def avatar_48_url( self ):
		avatar = self.avatars.filter( is_primary = True ).first()
		if avatar and avatar.avatar:
			return avatar.avatar_48x.url
		return static( 'main/img/avatar/avatar_015.png' )

	def __str__( self ):
		return f'{self.username} | {self.email}'

	class Meta:
		verbose_name = 'пользователь'
		verbose_name_plural = 'пользователи'
		ordering = ['username']


class UserAvatar( m.Model ):
	user = m.ForeignKey( User, on_delete = m.CASCADE, related_name = 'avatars', verbose_name = 'ID пользователя' )

	avatar = m.ImageField(
		upload_to = 'user_avatars', verbose_name = 'Аватар', null = True, blank = True,
		validators = [FileExtensionValidator( ['jpg', 'jpeg', 'png', 'webp'] )]
	)
	avatar_32x = ImageSpecField(
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

	is_primary  = m.BooleanField( default = False, verbose_name = 'Основной аватар' )
	uploaded_at = m.DateTimeField( auto_now_add = True, db_index = True, verbose_name = 'Время добавления' )

	def __str__(self):
		return f'Avatar of {self.user.username}'

	def save( self, *args, **kwargs ):
		if self.avatar:
			self.avatar_32x.generate()
			self.avatar_48x.generate()
			self.avatar_64x.generate()
			self.avatar_128x.generate()
			self.avatar_256x.generate()

		super().save( *args, **kwargs )

	class Meta:
		verbose_name = 'аватар'
		verbose_name_plural = 'аватары'
		ordering = [ 'user', '-uploaded_at' ]
		constraints = [
			m.UniqueConstraint(
				fields = ['user', 'is_primary'],
				condition = m.Q( is_primary = True ),
				name = 'one_primary_avatar'
			)
		]


SOCIAL_NETS = {
	'FB': 'Facebook',
	'GH': 'GitHub',
	'IG': 'Instagram',
	'LN': 'LinkedIn',
	'OK': 'Одноклассники',
	'PT': 'Pinterest',
	'RD': 'Reddit',
	'SC': 'Snapchat',
	'TG': 'Telegram',
	'TT': 'TikTok',
	'TW': 'Twitter',
	'VK': 'ВКонтакте',
	'WA': 'WhatsApp',
	'YT': 'YouTube',
}

class UserSocialLink( m.Model ):
	user        = m.ForeignKey( User, on_delete = m.CASCADE, related_name = 'social_links', verbose_name = 'ID пользователя' )
	network     = m.CharField( choices = SOCIAL_NETS, max_length = 2, verbose_name = 'Соцсеть' )
	link        = m.URLField( validators = [ URLValidator( schemes = ['http', 'https'] ) ], verbose_name = 'Ссылка' )
	description = m.CharField( max_length = 100, blank = True, verbose_name = 'Описание' )
	is_verified = m.BooleanField( default = False, verbose_name = 'Ссылка проверена' )
	is_primary  = m.BooleanField( default = False, verbose_name = 'Главная ссылка' )
	is_shown    = m.BooleanField( default = True,  verbose_name = 'Ссылка отображается' )
	created_at  = m.DateTimeField( auto_now_add = True, db_index = True, verbose_name = 'Дата/время записи' )
	updated_at  = m.DateTimeField( auto_now = True, verbose_name = 'Дата/время изменения' )

	def __str__(self):
		return f'Link to {self.network} from {self.user.username}'

	def clean( self ):
		super().clean()
		if validate_social_link( self.network, self.link ):
			self.is_verified = True

	class Meta:
		verbose_name = 'ссылка'
		verbose_name_plural = 'ссылки'
		ordering = ['user', '-created_at']
		constraints = [ m.UniqueConstraint( fields = ['user', 'network', 'is_primary'], name = 'one_primary_link' ) ]


class UserAddress( m.Model ):
	user    = m.ForeignKey( User, on_delete = m.CASCADE, db_index = True,
	                        related_name = 'addresses', verbose_name = 'ID пользователя' )
	address = m.ForeignKey( Address, on_delete = m.CASCADE, db_index = True,
	                        related_name = 'users', verbose_name = 'Адрес' )

	title = m.CharField( blank = True, null = True, verbose_name = 'Подпись', help_text = 'Дом, Работа и т.д.' )
	notes = m.TextField( blank = True, null = True, verbose_name = 'Заметки доставки' )

	is_default = m.BooleanField( default = False, verbose_name = 'Основной адрес' )

	created_at = m.DateTimeField( auto_now_add = True, db_index = True, verbose_name = 'Дата/время записи' )
	updated_at = m.DateTimeField( auto_now = True, verbose_name = 'Дата/время изменения' )

	@property
	def display_title( self ):
		"""Отображаемое название адреса"""
		if self.title:
			return self.title

		if self.is_default:
			return "Основной адрес"

		return f"Адрес #{self.pk}"

	def __str__(self):
		return f'Address of {self.user} - {self.address}'

	def save( self, *args, **kwargs ):
		if self.is_default:
			addresses_to_update = UserAddress.objects.filter( user = self.user, is_default = True )

			if self.pk:
				addresses_to_update = addresses_to_update.exclude( pk = self.pk )

			addresses_to_update.update( is_default = False )

		super().save( *args, **kwargs )

	class Meta:
		verbose_name = 'Адрес пользователя'
		verbose_name_plural = 'Адреса пользователей'
		ordering = ['-is_default', '-updated_at']
		constraints = [
			m.UniqueConstraint(
				fields = ['user', 'is_default'],
				condition = m.Q( is_default = True ),
				name = 'one_default_address_per_user'
			),
			m.UniqueConstraint(
				fields = ['user', 'address'],
				name = 'unique_address_per_user'
			)
		]
