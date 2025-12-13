from django.contrib import admin
from security.models import SecurityAction, SecurityNotice


@admin.register(SecurityAction)
class SecurityActionAdmin(admin.ModelAdmin):
	pass


@admin.register(SecurityNotice)
class SecurityNoticeAdmin(admin.ModelAdmin):
	pass
