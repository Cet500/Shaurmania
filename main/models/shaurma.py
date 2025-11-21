from django.db import models as m
from slugify import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Shaurma( m.Model ):
    name          = m.CharField( max_length = 60, unique = True, verbose_name = 'Название' )
    slug          = m.SlugField( max_length = 70, blank = True, verbose_name = "URL-адрес" )
    category      = m.ForeignKey( 'ShaurmaCategory', on_delete = m.SET_NULL,
                                       null = True, blank = True, verbose_name = 'Категория' )
    compound      = m.TextField( max_length = 600, verbose_name = 'Состав' )
    short_text    = m.TextField( max_length = 200, blank = True, verbose_name = 'Краткое описание' )
    description   = m.TextField( max_length = 1000, blank = True, verbose_name = 'Описание' )
    history       = m.TextField( max_length = 1000, blank = True, verbose_name = 'История' )
    picture       = m.ImageField( upload_to = 'shaurma_images', verbose_name = 'Изображение' )
    thumbnail_md  = ImageSpecField(
        source     = 'picture',
        processors = [ ResizeToFill( 640, 450) ],
        format     = 'PNG',
        options    = { 'quality': 90 },
    )
    thumbnail_sm  = ImageSpecField(
        source     = 'picture',
        processors = [ ResizeToFill( 285, 200) ],
        format     = 'PNG',
        options    = { 'quality': 90 },
    )
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

        if self.picture:
            self.thumbnail_md.generate()
            self.thumbnail_sm.generate()

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'шаурма'
        verbose_name_plural = 'шаурма'
        ordering = [ 'name' ]


class ShaurmaCategory( m.Model ):
    name        = m.CharField( max_length = 60,  verbose_name = 'Название' )
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


class ShaurmaImage( m.Model ):
    shaurma      = m.ForeignKey( Shaurma,  on_delete = m.CASCADE,  related_name = 'images', verbose_name = 'Шаурма' )
    image        = m.ImageField( upload_to = 'shaurma_additional', verbose_name = 'Изображение' )
    thumbnail_md = ImageSpecField(
        source     = 'image',
        processors = [ ResizeToFill( 550, 310 ) ],
        format     = 'PNG',
        options    = { 'quality': 90 },
    )
    caption      = m.CharField( default = 'Фото нашей шаурмы', max_length = 100,  blank = True,  verbose_name = 'Подпись' )
    order        = m.PositiveIntegerField( default = 0, verbose_name='Порядок отображения' )
    created_at   = m.DateTimeField( auto_now_add = True,  verbose_name = 'Дата добавления' )
    updated_at   = m.DateTimeField( auto_now = True, verbose_name = "Дата обновления" )

    def save( self, *args, **kwargs ):
        super().save( *args, **kwargs )

        if self.image:
            self.thumbnail_md.generate()

    def __str__(self):
        return f'Изображение {self.id} для {self.shaurma.name}'

    class Meta:
        verbose_name = 'изображение шаурмы'
        verbose_name_plural = 'изображения шаурмы'
        ordering = ['shaurma', 'order']
