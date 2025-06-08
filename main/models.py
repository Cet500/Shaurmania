import uuid
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from slugify import slugify


class Review( models.Model ):
    name    = models.CharField( max_length = 60,  verbose_name = 'Имя' )
    text    = models.TextField( max_length = 600, verbose_name = 'Текст отзыва' )
    stars   = models.SmallIntegerField( validators = [ MinValueValidator(1), MaxValueValidator(5) ],
                                        verbose_name = 'Оценка' )
    shaurma = models.ForeignKey( 'Shaurma', on_delete = models.SET_NULL,
                                 null = True, blank = True, verbose_name = 'Шаурма' )
    date    = models.DateTimeField( auto_now_add = True, verbose_name = 'Время записи' )

    def __str__(self):
        return f'Отзыв от {self.name} ( {self.stars} / 5 )'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = [ 'name' ]


class Shaurma( models.Model ):
    name          = models.CharField( max_length = 60, unique = True, verbose_name = 'Название' )
    slug          = models.SlugField( max_length = 70, blank = True, verbose_name = "URL-адрес" )
    category      = models.ForeignKey( 'ShaurmaCategory', on_delete = models.SET_NULL,
                                       null = True, blank = True, verbose_name = 'Категория' )
    compound      = models.TextField( max_length = 600, verbose_name = 'Состав' )
    short_text    = models.TextField( max_length = 200, blank = True, verbose_name = 'Краткое описание' )
    description   = models.TextField( max_length = 1000, blank = True, verbose_name = 'Описание' )
    picture       = models.ImageField( upload_to = 'shaurma_images', verbose_name = 'Изображение' )
    price         = models.PositiveSmallIntegerField( verbose_name = 'Цена в ₽' )
    weight        = models.PositiveSmallIntegerField( verbose_name = 'Вес в гр' )
    calories      = models.PositiveIntegerField( default = 0, verbose_name = "Калории (ккал)" )
    proteins      = models.FloatField( default = 0, verbose_name = "Белки (г)" )
    fats          = models.FloatField( default = 0, verbose_name = "Жиры (г)" )
    carbohydrates = models.FloatField( default = 0, verbose_name = "Углеводы (г)" )
    is_available  = models.BooleanField( default = True, verbose_name = "Доступна для заказа" )
    created_at    = models.DateTimeField( auto_now_add = True, verbose_name = "Дата создания" )
    updated_at    = models.DateTimeField( auto_now = True, verbose_name = "Дата обновления" )

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


class ShaurmaCategory( models.Model ):
    name        = models.CharField( max_length = 60, verbose_name = 'Название' )
    description = models.TextField( max_length = 200, verbose_name = 'Описание' )
    order       = models.PositiveSmallIntegerField( default = 0, verbose_name = "Порядок сортировки" )
    created_at  = models.DateTimeField( auto_now_add = True, verbose_name = "Дата создания" )
    updated_at  = models.DateTimeField( auto_now = True, verbose_name = "Дата обновления" )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория шаурмы'
        verbose_name_plural = 'категории шаурмы'
        ordering = [ 'order', 'name' ]


class Location( models.Model ):
    address     = models.CharField( max_length = 60,  verbose_name = 'Адрес' )
    description = models.TextField( max_length = 600, verbose_name = 'Описание' )
    picture     = models.ImageField( upload_to = 'locations', verbose_name = 'Изображение' )
    name        = models.CharField( max_length = 60, verbose_name = 'Название' )
    contacts    = models.CharField( max_length = 18, verbose_name = 'Номер' )
    city        = models.CharField( max_length = 30, verbose_name = 'Город' )
    open_hours  = models.TimeField( verbose_name = 'Начало' )
    close_hours = models.TimeField( verbose_name = 'Конец' )
    
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
    username     = models.CharField( max_length = 60, unique = True, verbose_name = 'Никнейм' )
    picture      = models.ImageField( upload_to = 'user_images', verbose_name = 'Изображение' )
    email        = models.EmailField( max_length = 80, verbose_name = 'Email' )
    number       = models.CharField( max_length = 17, verbose_name = 'Номер' )
    last_address = models.CharField( max_length = 200, verbose_name = 'Адрес последней доставки' )
    reg_date     = models.DateTimeField( auto_now_add = True, verbose_name = 'время регистрации' )

    is_open   = models.BooleanField( default = True, verbose_name = 'Открытый профиль?' )
    is_active = models.BooleanField( default = True, verbose_name = 'Профиль активен?' )
    is_staff  = models.BooleanField( default = False, verbose_name = 'Это сотрудник сайта?' )

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


class Order( models.Model ):
    ORDER_STATUS_CHOICES = [
        ('carted', 'В корзине'),
        ('cancelled', 'Отменен'),
        ('ordered', 'Куплен'),
        ('completed', 'Завершен'),
    ]

    user    = models.ForeignKey( 'User', on_delete = models.CASCADE, verbose_name = 'Пользователь' )
    status  = models.CharField( max_length = 20, choices = ORDER_STATUS_CHOICES, default = 'carted', verbose_name = 'Статус')
    date    = models.DateTimeField( auto_now_add = True )


    def __str__(self):
        return f'Заказ {self.id} от {self.user.username} - Статус: {self.status}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ['id']

class Achievement( models.Model ):
    name    = models.CharField( max_length = 60, verbose_name = 'Название' )
    picture = models.ImageField( upload_to = 'achievement_image', verbose_name = 'Изображение' )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'достижение'
        verbose_name_plural = 'достижения'
        ordering = [ 'name' ]


class UserAchievement( models.Model ):
    user        = models.ForeignKey( 'User', on_delete = models.CASCADE, verbose_name = 'Пользователь' )
    achievement = models.ForeignKey( 'Achievement', on_delete = models.CASCADE, verbose_name = 'Достижение' )
    get_date    = models.DateTimeField( auto_now_add = True, verbose_name = 'Время получения' )

    def __str__(self):
        return f'{self.user.username} - {self.achievement.name}'

    class Meta:
        verbose_name = 'достижение пользователя'
        verbose_name_plural = 'достижения пользователей'
        ordering = [ 'get_date' ]


class Stock( models.Model ):
    name        = models.CharField( max_length = 60, verbose_name = 'Название' )
    short_text  = models.CharField( max_length = 150, blank = True, verbose_name = 'Краткое описание' )
    description = models.TextField( max_length = 1000, blank = True, verbose_name = 'Описание' )
    condition   = models.TextField( max_length = 1000, blank = True, verbose_name = 'Условия акции' )
    image       = models.ImageField( upload_to = 'stocks', verbose_name = 'Изображение' )
    discount    = models.SmallIntegerField( verbose_name = 'Скидка в %' )
    categories  = models.ManyToManyField( 'ShaurmaCategory', blank = True, verbose_name = 'Категория' )
    date_start  = models.DateField( verbose_name = 'Старт' )
    date_end    = models.DateField( verbose_name = 'Завершение' )

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'акция'
        verbose_name_plural = 'акции'
        ordering = [ 'name' ]


class Promocode( models.Model ):
    code_name = models.CharField( max_length = 20, unique = True, verbose_name = 'Промокод' )
    code_uuid = models.UUIDField( default=uuid.uuid4, editable=False, verbose_name = 'Промокод UUID' )
    duration  = models.SmallIntegerField( default = 7, verbose_name = 'Время жизни ( в днях )' )
    discount  = models.SmallIntegerField( default = 5, verbose_name = 'Скидка в %' )
    date_add  = models.DateField( verbose_name = 'Дата создания' )
    date_end  = models.DateField( null = True, blank = True, editable=False, verbose_name = 'Дата конца' )

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
