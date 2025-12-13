from django.contrib import admin
from security.models import SecurityDevice, SecurityAuthLog


@admin.register(SecurityDevice)
class SecurityDeviceAdmin(admin.ModelAdmin):
	pass


@admin.register(SecurityAuthLog)
class SecurityAuthLogAdmin(admin.ModelAdmin):
	pass
