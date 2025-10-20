from django.contrib import admin
from .models import Review, Shaurma, Location, User, Order, Achievement, UserAchievement, Stock, Cart
from django.utils.safestring import mark_safe

from main.models import Promocode, ShaurmaCategory, ShaurmaImage


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'text', 'get_stars', 'shaurma', 'date' ]
    list_display_links = [ 'name' ]
    list_filter = [ 'stars', 'date' ]
    list_editable = [  ]

    def get_stars( self, obj ):
        return f'{obj.stars} {'★' * obj.stars}'

    get_stars.short_description = 'Оценка'


@admin.register(Shaurma)
class ShaurmaAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'name', 'get_picture', 'compound', 'category', 'get_energy_value', 'get_price', 'get_weight', 'created_at' ]
    list_display_links = [ 'name' ]
    list_filter = [ 'created_at' ]

    def get_picture( self, obj ):
        if obj.picture:
            return mark_safe( f'<img src="{obj.picture.url}" width="100" />' )
        else:
            return mark_safe( f'<b>нет</b>' )

    get_picture.short_description = 'Изображение'

    def get_energy_value( self, obj ):
        return f'{obj.calories} ккал   {obj.proteins} / {obj.fats} / {obj.carbohydrates}'

    get_energy_value.short_description = 'Данные КБЖУ'

    def get_price( self, obj ):
        return f'{obj.price} ₽'

    get_price.short_description = 'Цена в ₽'

    def get_weight( self, obj ):
        return f'{obj.weight} гр'

    get_weight.short_description = 'Вес в гр'


class ShaurmaInline( admin.TabularInline  ):
    model = Shaurma
    extra = 0
    fields = [ 'name', 'price', 'weight', 'calories', 'is_available', 'created_at' ]
    readonly_fields = [ 'name', 'created_at' ]
    show_change_link = True
    can_delete = False
    can_add = False


@admin.register( ShaurmaCategory )
class ShaurmaCategoryAdmin( admin.ModelAdmin ):
    list_display       = [ 'name', 'shaurma_count', 'description', 'created_at' ]
    list_display_links = [ 'name' ]
    list_filter        = [ 'created_at' ]

    inlines = [ ShaurmaInline ]

    def shaurma_count( self, obj ):
        return obj.shaurma_set.count()

    shaurma_count.short_description = "Размер"


@admin.register( ShaurmaImage )
class ShaurmaImageAdmin( admin.ModelAdmin ):
    list_display       = [ 'shaurma', 'caption', 'get_image', 'created_at' ]
    list_display_links = [ 'shaurma' ]
    list_filter        = [ 'shaurma', 'created_at' ]

    def get_image( self, obj ):
        if obj.image:
            return mark_safe( f'<img src="{obj.image.url}" width="200" />' )
        else:
            return mark_safe( f'<b>нет</b>' )

    get_image.short_description = 'Изображение'


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

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quanity')  # было 'shaurma' — заменено на 'item' и 'quanity' (как в модели)
    list_filter = ('user',)
    search_fields = ('user__username', 'item__name')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'picture']


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'get_date']
    list_filter  = ['get_date']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'get_image', 'short_text', 'display_categories', 'get_discount', 'get_dates' ]
    # filter_horizontal = [ 'categories', ]

    def get_image( self, obj ):
        if obj.image:
            return mark_safe( f'<img src="{obj.image.url}" width="100" />' )
        else:
            return mark_safe( f'<b>нет</b>' )

    get_image.short_description = 'Изображение'

    def display_categories( self, obj ):
        return ", ".join( [category.name for category in obj.categories.all()] )

    display_categories.short_description = 'Категории'

    def get_discount( self, obj ):
        return f'{obj.discount} %'

    get_discount.short_description = 'Скидка'

    def get_dates( self, obj ):
        if obj.date_start == obj.date_end:
            return f'{obj.date_end}'
        else:
            return f'{obj.date_start} - {obj.date_end}'

    get_dates.short_description = 'Время акции'

@admin.register( Promocode )
class PromocodeAdmin( admin.ModelAdmin ):
    list_display = [ 'code_name', 'code_uuid', 'duration', 'discount', 'date_add', 'date_end' ]
    list_filter = [ 'date_add', 'date_end' ]
