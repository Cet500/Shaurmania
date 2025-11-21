from django.db import models as m


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
