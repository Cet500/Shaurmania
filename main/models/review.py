from django.db import models as m
from django.core.validators import MinValueValidator,MaxValueValidator


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
