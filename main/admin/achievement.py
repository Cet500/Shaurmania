from django.contrib import admin
from main.models import Achievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
	list_display = ['name', 'picture']
