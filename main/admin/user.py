from django.contrib import admin
from main.models import User, UserAchievement


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = [ 'username', 'picture', 'number', 'email', 'last_address', 'reg_date' ]
	list_filter  = [ 'reg_date' ]


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
	list_display = ['user', 'achievement', 'get_date']
	list_filter  = ['get_date']
