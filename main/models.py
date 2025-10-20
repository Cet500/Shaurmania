import uuid
from django.db import models as m
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from slugify import slugify


class Review( m.Model ):
    name    = m.CharField( max_length = 60,  verbose_name = 'Имя' )
    text    = m.TextField( max_length = 600, verbose_name = 'Текст отзыва' )
    stars   = m.SmallIntegerField( validators = [ MinValueValidator(1), MaxValueValidator(5) ],
                                        verbose_name = 'Оценка' )
    shaurma = m.ForeignKey( 'Shaurma', on_delete = m.SET_NULL,
                                 null = True, blank = True, verbose_name = 'Шаурма' )
    date    = m.DateTimeField( auto_now_add = True, verbose_name = 'Время записи' )

    def __str__(self):
        return f'Отзыв от {self.name} ( {self.stars} / 5 )'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = [ 'name' ]


class Shaurma( m.Model ):
    name          = m.CharField( max_length = 60, unique = True, verbose_name = 'Название' )
    slug          = m.SlugField( max_length = 70, blank = True, verbose_name = "URL-адрес" )
    category      = m.ForeignKey( 'ShaurmaCategory', on_delete = m.SET_NULL,
                                       null = True, blank = True, verbose_name = 'Категория' )
    compound      = m.TextField( max_length = 600, verbose_name = 'Состав' )
    short_text    = m.TextField( max_length = 200, blank = True, verbose_name = 'Краткое описание' )
    description   = m.TextField( max_length = 1000, blank = True, verbose_name = 'Описание' )
    picture       = m.ImageField( upload_to = 'shaurma_images', verbose_name = 'Изображение' )
    price         = m.PositiveSmallIntegerField( verbose_name = 'Цена в ₽' )
    weight        = m.PositiveSmallIntegerField( verbose_name = 'Вес в гр' )
    calories      = m.PositiveIntegerField( default = 0, verbose_name = "Калории (ккал)" )
    proteins      = m.FloatField( default = 0, verbose_name = "Белки (г)" )
    fats          = m.FloatField( default = 0, verbose_name = "Жиры (г)" )
    carbohydrates = m.FloatField( default = 0, verbose_name = "Углеводы (г)" )
    is_available  = m.BooleanField( default = True, verbose_name = "Доступна для заказа" )
    created_at    = m.DateTimeField( auto_now_add = True, verbose_name = "Дата создания" )
    updated_at    = m.DateTimeField( auto_now = True, verbose_name = "Дата обновления" )

    def save( self, *args, **kwargs ):
        if not self.slug:
            self.slug = slugify( self.name )
        super().save( *args, **kwargs )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'шаурма'
        verbose_name_plural = 'шаурма'
        ordering = [ 'name' ]


class ShaurmaCategory( m.Model ):
    name        = m.CharField( max_length = 60, verbose_name = 'Название' )
    description = m.TextField( max_length = 200, verbose_name = 'Описание' )
    order       = m.PositiveSmallIntegerField( default = 0, verbose_name = "Порядок сортировки" )
    created_at  = m.DateTimeField( auto_now_add = True, verbose_name = "Дата создания" )
    updated_at  = m.DateTimeField( auto_now = True, verbose_name = "Дата обновления" )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория шаурмы'
        verbose_name_plural = 'категории шаурмы'
        ordering = [ 'order', 'name' ]


class Location( m.Model ):
    address     = m.CharField( max_length = 60,  verbose_name = 'Адрес' )
    description = m.TextField( max_length = 600, verbose_name = 'Описание' )
    picture     = m.ImageField( upload_to = 'locations', verbose_name = 'Изображение' )
    name        = m.CharField( max_length = 60, verbose_name = 'Название' )
    contacts    = m.CharField( max_length = 18, verbose_name = 'Номер' )
    city        = m.CharField( max_length = 30, verbose_name = 'Город' )
    open_hours  = m.TimeField( verbose_name = 'Начало' )
    close_hours = m.TimeField( verbose_name = 'Конец' )
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'заведениe'
        verbose_name_plural = 'заведения'
        ordering = [ 'address' ]


class UserManager( BaseUserManager ):
    def create_user(self, email, username, password, **extra_fields):
        if not username:
            raise ValueError('Введите имя пользователя')
        
        if not email:
            raise ValueError('Это не Email')
        
        email = self.normalize_email(email)
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

    USERNAME_FIELD  = 'username'
    EMAIL_FIELD     = 'email'
    REQUIRED_FIELDS = [ 'email' ]

    def __str__(self):
        return f'{self.username} | {self.email}'
    
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = [ 'username' ]


class Order( m.Model ):
    user    = m.ForeignKey( 'User', on_delete = m.CASCADE, verbose_name = 'Пользователь' )
    shaurma = m.ForeignKey( 'Shaurma', on_delete = m.CASCADE, verbose_name = 'Шаурма' )
    date    = m.DateTimeField( auto_now_add = True )

    def __str__(self):
        return f'Заказ {self.shaurma.name} от {self.user.username}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

class Cart( m.Model ):
    user = m.ForeignKey( 'User', on_delete = m.CASCADE, verbose_name='Пользователь' )
    item = m.ForeignKey( 'Shaurma', on_delete = m.CASCADE, verbose_name = 'Шаурма' )
    quanity = m.PositiveSmallIntegerField( 'Quanity', default=1 )

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'


class Achievement( m.Model ):
    name    = m.CharField( max_length = 60, verbose_name = 'Название' )
    picture = m.ImageField( upload_to = 'achievement_image', verbose_name = 'Изображение' )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'достижение'
        verbose_name_plural = 'достижения'
        ordering = [ 'name' ]


class UserAchievement( m.Model ):
    user        = m.ForeignKey( 'User', on_delete = m.CASCADE, verbose_name = 'Пользователь' )
    achievement = m.ForeignKey( 'Achievement', on_delete = m.CASCADE, verbose_name = 'Достижение' )
    get_date    = m.DateTimeField( auto_now_add = True, verbose_name = 'Время получения' )

    def __str__(self):
        return f'{self.user.username} - {self.achievement.name}'

    class Meta:
        verbose_name = 'достижение пользователя'
        verbose_name_plural = 'достижения пользователей'
        ordering = [ 'get_date' ]


class Stock( m.Model ):
    slug        = m.SlugField( max_length = 70, blank = True, verbose_name = "URL-адрес" )
    name        = m.CharField( max_length = 60, verbose_name = 'Название' )
    short_text  = m.CharField( max_length = 150, blank = True, verbose_name = 'Краткое описание' )
    description = m.TextField( max_length = 1000, blank = True, verbose_name = 'Описание' )
    condition   = m.TextField( max_length = 1000, blank = True, verbose_name = 'Условия акции' )
    image       = m.ImageField( upload_to = 'stocks', verbose_name = 'Изображение' )
    discount    = m.SmallIntegerField( verbose_name = 'Скидка в %' )
    categories  = m.ManyToManyField( 'ShaurmaCategory', blank = True, verbose_name = 'Категория' )
    date_start  = m.DateField( verbose_name = 'Старт' )
    date_end    = m.DateField( verbose_name = 'Завершение' )

    def save( self, *args, **kwargs ):
        if not self.slug:
            self.slug = slugify( self.name )
        super().save( *args, **kwargs )

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'акция'
        verbose_name_plural = 'акции'
        ordering = [ 'name' ]


class Promocode( m.Model ):
    code_name = m.CharField( max_length = 20, unique = True, verbose_name = 'Промокод' )
    code_uuid = m.UUIDField( default=uuid.uuid4, editable=False, verbose_name = 'Промокод UUID' )
    duration  = m.SmallIntegerField( default = 7, verbose_name = 'Время жизни ( в днях )' )
    discount  = m.SmallIntegerField( default = 5, verbose_name = 'Скидка в %' )
    date_add  = m.DateField( verbose_name = 'Дата создания' )
    date_end  = m.DateField( null = True, blank = True, editable=False, verbose_name = 'Дата конца' )

    def save( self, *args, **kwargs ):
        if not self.id:
            self.date_end = self.date_add + timezone.timedelta( days = self.duration )

        super().save( *args, **kwargs )

    def __str__(self):
        return f'{self.code_name} ( {self.duration}d / {self.discount}%) )'

    class Meta:
        verbose_name = 'промокод'
        verbose_name_plural = 'промокоды'
        ordering = [ '-date_end' ]
