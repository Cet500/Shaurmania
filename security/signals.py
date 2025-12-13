from datetime import datetime

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from geodata.utils import get_country_by_ip
from security.models import SecurityDevice, SecurityAuthLog
from .utils import get_client_ip


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    ip = get_client_ip(request)
    country = get_country_by_ip(ip)
    user_agent_str = request.META.get('HTTP_USER_AGENT', '')

    device = SecurityDevice.from_user_agent(user_agent_str)
    device.save()

    # Здесь можно попытаться получить UUID из cookie/localStorage запроса
    # Для упрощения - не показано, нужно реализовать в middleware/на фронте
    # Например: device_uuid = request.COOKIES.get('device_uuid')

    SecurityAuthLog.objects.create(
        user        = user,
        device      = device,
        ip_address  = ip,
        geo_country = country,
        is_success  = True
    )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    # Найти последний лог без logout_at и обновить logout_at
    if not user:
        return

    last_log = SecurityAuthLog.objects.filter(user=user, logout_at__isnull=True).order_by('-login_at').first()

    if last_log:
        last_log.logout_at = datetime.now()
        last_log.save()
