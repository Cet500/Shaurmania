from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator


class Review( models.Model ):
    name    = models.CharField( max_length = 60,  verbose_name = 'Имя' )
    text    = models.TextField( max_length = 600, verbose_name = 'Текст отзыва' )
    stars   = models.SmallIntegerField( validators = [ MinValueValidator(1), MaxValueValidator(5) ],
                                      verbose_name = 'Оценка' )
    shaurma = models.ForeignKey( 'Shaurma', on_delete = models.PROTECT, default = 3, verbose_name = 'Шаурма' )
    date    = models.CharField( max_length = 30, verbose_name = 'Дата/Время записи' )

    def __str__(self):
        return f"Отзыв от {self.name} ( {self.stars} / 5 )"

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

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'шаурма'
        verbose_name_plural = 'шаурма'
        ordering = ['name']


class Location( models.Model ):
    address     = models.CharField( max_length = 60,  verbose_name = 'Адрес' )
    description = models.TextField( max_length = 600, verbose_name = 'Описание' )
    picture = models.ImageField( upload_to = 'locations', verbose_name = 'Изображение' )
    name = models.CharField( max_length=60, verbose_name = "Название")
    сontacts = models.CharField( max_length = 18, verbose_name = 'Номер' )
    city = models.CharField( max_length = 30, verbose_name = 'Город')
    opening_hours = models.CharField( max_length= 20, verbose_name='Время работы')
    
    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'заведениe'
        verbose_name_plural = 'заведения'
        ordering = ['address']


class User( models.Model ):
    username = models.CharField( max_length = 60, verbose_name = 'Юзернейм' )
    picture = models.ImageField( upload_to = 'user_images', verbose_name = 'Изображение' )
    email = models.EmailField( max_length = 80 )
    number = models.CharField( max_length = 12, verbose_name = 'Номер' )
    last_address = models.CharField( max_length = 200, verbose_name = "Адрес последней доставки" )
    reg_date = models.DateTimeField( auto_now_add = True )




class Order( models.Model ):
    user = models.ForeignKey( 'User', on_delete = models.CASCADE, verbose_name = 'Пользователь' )
    shaurma = models.ForeignKey( 'Shaurma', on_delete = models.CASCADE, verbose_name = 'Шаурма' )
    date = models.DateTimeField(auto_now_add = True)


class Achievement( models.Model ):
    name = models.CharField( max_length=60, verbose_name = "Название")
    picture = models.ImageField( upload_to = "achievement_image", verbose_name = "Изображение" )


class UserAchievement( models.Model ):
    user = models.ForeignKey( 'User', on_delete = models.CASCADE, verbose_name = 'Пользователь')
    achievement = models.ForeignKey( 'Achievement', on_delete = models.CASCADE, verbose_name = 'Достижение')
    get_date = models.DateTimeField(auto_now_add = True)


class Stock( models.Model ):
    name = models.CharField( max_length=60, verbose_name = "Название")
    description = models.CharField( max_length=150, verbose_name= "Описание")
    discount = models.SmallIntegerField( verbose_name="Скидка в %")
    product = models.CharField( max_length=40, verbose_name="Товар")
    сondition = models.CharField( max_length=40, verbose_name="Условие")
    date_start = models.DateTimeField(auto_now_add = True)
    date_end = models.DateTimeField()

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'акция'
        verbose_name_plural = 'акции'
        ordering = ['name']
