from django.contrib import admin
from django.utils.safestring import mark_safe
from main.models import News, NewsTag


@admin.register( News )
class NewsAdmin( admin.ModelAdmin ):
	list_display       = [ 'title', 'get_picture', 'short_text', 'created_at', 'updated_at' ]
	list_display_links = [ 'title' ]
	list_filter        = [ 'is_shown', 'is_important', 'created_at', 'updated_at' ]
	filter_horizontal  = [ 'tags' ]
	search_fields      = [ 'title', 'short_text', 'main_text' ]
	readonly_fields    = [ 'get_picture_big', 'created_at', 'updated_at' ]

	fieldsets = (
		('Основное', {
			'fields': ('title', 'slug', 'short_text')
		}),
		('Статья', {
			'fields': ('rich_content',)
		}),
		('Изображение', {
			'fields': ('picture', 'get_picture_big'),
		}),
		('Настройки', {
			'fields': ('is_shown', 'is_important', 'tags')
		}),
		('Даты', {
			'fields': ('created_at', 'updated_at'),
		}),
	)

	def get_picture( self, obj ):
		if obj.picture:
			return mark_safe( f'<img src="{obj.picture.url}" width="200" />' )
		else:
			return mark_safe( f'<b>нет</b>' )

	get_picture.short_description = 'Изображение'

	def get_picture_big( self, obj ):
		if obj.picture:
			return mark_safe( f'<img src="{obj.picture.url}" width="500" />' )
		else:
			return mark_safe( f'<b>нет</b>' )

	get_picture_big.short_description = 'Изображение'

	class Media:
		css = {
			'all': (
				'main/assets/sceditor/themes/square.min.css',
			)
		}
		js = (
			'main/assets/sceditor/sceditor.min.js',
			'main/assets/sceditor/icons/monocons.min.js',
			'main/assets/sceditor/formats/xhtml.min.js',
			'main/assets/sceditor/languages/ru.min.js',
			'main/js/src/sceditor_init.js'
		)


class NewsInline( admin.TabularInline  ):
	model = News.tags.through
	extra = 0
	fields = [ 'get_news_title', 'get_short_text', 'get_is_shown', 'get_created_at' ]
	readonly_fields = [ 'get_news_title', 'get_short_text', 'get_is_shown', 'get_created_at' ]
	show_change_link = False
	can_delete = False
	can_add = False

	def get_news_title( self, obj ):
		return obj.news.title

	get_news_title.short_description = 'Заголовок'

	def get_short_text( self, obj ):
		return obj.news.short_text

	get_short_text.short_description = 'Краткое описание'

	def get_is_shown( self, obj ):
		return obj.news.is_shown

	get_is_shown.short_description = 'Показывается'

	def get_created_at( self, obj ):
		return obj.news.created_at

	get_created_at.short_description = 'Дата создания'


@admin.register( NewsTag )
class NewsTagAdmin( admin.ModelAdmin ):
	list_display       = [ 'name', 'news_count', 'created_at' ]
	list_display_links = [ 'name' ]
	list_filter        = [ 'created_at' ]

	inlines = [ NewsInline ]

	def news_count( self, obj ):
		return obj.news_set.count()

	news_count.short_description = "Новостей"
