from django.contrib import admin
from.models import Review, Shaurma, Location, User, Order, Achievement, UserAchievement
from django.utils.safestring import mark_safe


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'text', 'get_stars', 'shaurma', 'date' ]
    list_display_links = [ 'name' ]
    list_filter = [ 'stars' ]
    list_editable = [ 'shaurma' ]

    def get_stars( self, obj ):
        return f'{obj.stars} {'★' * obj.stars}'

    get_stars.short_description = 'Оценка'


@admin.register(Shaurma)
class ShaurmaAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'get_picture', 'description', 'get_price', 'get_weight']
    list_display_links = ['name']

    def get_picture( self, obj ):
        if obj.picture:
            return mark_safe( f'<img src="{obj.picture.url}" width="100" />' )
        else:
            return mark_safe( f'<b>нет</b>' )

    get_picture.short_description = 'Изображение'

    def get_price( self, obj ):
        return f'{obj.price} ₽'

    get_price.short_description = 'Цена в ₽'

    def get_weight( self, obj ):
        return f'{obj.weight} гр'

    get_weight.short_description = 'Вес в гр'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [ 'address', 'description' ]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [ 'username', 'picture', 'number', 'email', 'last_address', 'reg_date' ]
    list_filter  = [ 'reg_date' ]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'shaurma', 'date']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'picture']


@admin.register(UserAchievement)
class UserAchievement(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'get_date']
    list_filter  = ['get_date']