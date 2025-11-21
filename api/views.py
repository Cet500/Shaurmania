from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from main.factories import (
    ShaurmaFactory,
    ShaurmaCategoryFactory,
    ShaurmaImageFactory,
    LocationFactory,
    UserFactory,
    AchievementFactory,
    UserAchievementFactory,
    ReviewFactory,
    StockFactory,
)


FACTORY_REGISTRY = {
    'shaurma': ShaurmaFactory,
    'shaurma_category': ShaurmaCategoryFactory,
    'shaurma_image': ShaurmaImageFactory,
    'location': LocationFactory,
    'user': UserFactory,
    'achievement': AchievementFactory,
    'user_achievement': UserAchievementFactory,
    'review': ReviewFactory,
    'stock': StockFactory,
}


def _to_jsonable(value):
    import datetime
    try:
        from django.db.models import Model
    except Exception:
        Model = object  # fallback, should not happen in Django context

    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (datetime.date, datetime.datetime, datetime.time)):
        return value.isoformat()
    if isinstance(value, Model):
        return str(value)
    return str(value)


def _serialize_factory_object(obj):
    exclude_keys = { '_state', '_ik', 'picture', 'image', 'password', '_prefetched_objects_cache' }
    data = {}
    for key, val in obj.__dict__.items():
        if key in exclude_keys:
            continue
        data[key] = _to_jsonable(val)
    return data


@login_required
def admin_factories(request):
    if not request.user.is_superuser:
        return JsonResponse({ 'detail': 'Forbidden' }, status = 403)

    return JsonResponse({
        'available_factories': sorted(list(FACTORY_REGISTRY.keys()))
    })


@login_required
def admin_factory_generate(request, name):
    if not request.user.is_superuser:
        return JsonResponse({ 'detail': 'Forbidden' }, status = 403)

    factory_cls = FACTORY_REGISTRY.get(name)
    if not factory_cls:
        return JsonResponse({ 'detail': 'Factory not found' }, status = 404)

    try:
        count = int(request.GET.get('count', '1'))
    except ValueError:
        count = 1
    count = max(1, min(count, 50))  # simple safety cap

    items = []
    for _ in range(count):
        obj = factory_cls.build()
        items.append(_serialize_factory_object(obj))

    return JsonResponse({ 'factory': name, 'count': len(items), 'items': items })
