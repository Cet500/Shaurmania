import uuid

from django.utils import timezone
from django.db import models as m


class Order( m.Model ):
    user    = m.ForeignKey( 'main.User', on_delete = m.CASCADE, verbose_name = 'Пользователь' )
    shaurma = m.ForeignKey( 'main.Shaurma', on_delete = m.CASCADE, verbose_name = 'Шаурма' )
    date    = m.DateTimeField( auto_now_add = True )

    def __str__(self):
        return f'Заказ {self.shaurma.name} от {self.user.username}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class Cart( m.Model ):
    user = m.ForeignKey( 'main.User', on_delete = m.CASCADE, verbose_name='Пользователь' )
    item = m.ForeignKey( 'main.Shaurma', on_delete = m.CASCADE, verbose_name = 'Шаурма' )
    quanity = m.PositiveSmallIntegerField( 'Quanity', default=1 )

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'


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
