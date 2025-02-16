from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator


class Review( models.Model ):
    name  = models.CharField( max_length = 60,  verbose_name = 'Имя' )
    text  = models.TextField( max_length = 600, verbose_name = 'Текст отзыва' )
    stars = models.SmallIntegerField( validators = [ MinValueValidator(1), MaxValueValidator(5) ],
                                      verbose_name = 'Оценка' )
    date  = models.CharField( max_length = 30, verbose_name = 'Дата/Время записи' )

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = [ 'name' ]


class Shaurma( models.Model ):
    name        = models.CharField( max_length = 60,  verbose_name = 'Название' )
    compound    = models.TextField( max_length = 600, verbose_name = 'Состав' )
    description = models.TextField( max_length = 600, verbose_name = 'Описание' )
    picture     = models.ImageField( upload_to = 'shaurma_images', verbose_name = 'Изображение' )
    price       = models.PositiveSmallIntegerField( verbose_name = 'Цена в ₽' )
    weight      = models.PositiveSmallIntegerField( verbose_name = 'Вес в гр' )

    class Meta:
        verbose_name = 'шаурма'
        verbose_name_plural = 'шаурма'
        ordering = ['name']


class Location( models.Model ):
    address     = models.CharField( max_length = 60,  verbose_name = 'Адрес' )
    description = models.TextField( max_length = 600, verbose_name = 'Описание' )
    
    class Meta:
        verbose_name = 'заведениe'
        verbose_name_plural = 'заведения'
        ordering = ['address']


class User( models.Model ):
    username = models.CharField( max_length = 60, verbose_name = 'Юзернейм' )
    picture = models.ImageField( upload_to = 'user_images', verbose_name = 'Изображение' )


class Order( models.Model ):
    user = models.ForeignKey( 'User', on_delete = models.CASCADE, verbose_name = 'Пользователь' )
    shaurma = models.ForeignKey( 'Shaurma', on_delete = models.CASCADE, verbose_name = 'Шаурма' )
    date = models.DateTimeField(auto_now_add = True)
