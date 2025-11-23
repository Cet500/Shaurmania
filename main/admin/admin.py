import json

from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.utils.safestring import mark_safe
from django.db.migrations.recorder import MigrationRecorder


# ================================ SESSIONS ================================== #


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
	list_display = ['session_key', 'session_data_open', 'expire_date']
	list_filter = ['expire_date']
	readonly_fields = ['session_key', 'session_data_open', 'session_data', 'expire_date']
	search_fields = ['session_key']

	def session_data_open(self, obj):
		session_store = SessionStore(session_key=obj.session_key)
		session_data = session_store.load()
		formatted_data = json.dumps(session_data, indent=4)
		return mark_safe('<pre>{}</pre>'.format(formatted_data))

	session_data_open.short_description = 'Открытые данные сессии'

	def has_add_permission(self, request):
		return False

	def has_change_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return False


# ================================ MIGRATION ================================= #


@admin.register( MigrationRecorder.Migration )
class MigrationAdmin( admin.ModelAdmin ):
	list_display = [ 'id', 'app', 'name', 'applied' ]
	list_display_links = ['id']
	list_filter = ['applied', 'app']
	search_fields = ['app', 'name']
	list_per_page = 100
	date_hierarchy = 'applied'
