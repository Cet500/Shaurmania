# Оптимизация

## Оптимизация запросов к БД

### select_related

Используйте для ForeignKey связей (JOIN):

```python
# Плохо (N+1 запрос)
shaurmas = Shaurma.objects.all()
for shaurma in shaurmas:
    print(shaurma.category.name)  # Отдельный запрос для каждой

# Хорошо (1 запрос)
shaurmas = Shaurma.objects.select_related('category').all()
for shaurma in shaurmas:
    print(shaurma.category.name)  # Данные уже загружены
```

### prefetch_related

Используйте для ManyToMany и обратных ForeignKey:

```python
# Плохо (N+1 запрос)
news_list = News.objects.all()
for news in news_list:
    print(news.tags.all())  # Отдельный запрос для каждой

# Хорошо (2 запроса)
news_list = News.objects.prefetch_related('tags').all()
for news in news_list:
    print(news.tags.all())  # Данные уже загружены
```

### Комбинация

```python
shaurmas = Shaurma.objects.select_related('category').prefetch_related('images', 'reviews').all()
```

### only() и defer()

Загружайте только нужные поля:

```python
# Загрузить только нужные поля
users = User.objects.only('username', 'email').all()

# Исключить ненужные поля
users = User.objects.defer('description').all()
```

## Индексы в БД

Добавляйте индексы для часто используемых полей:

```python
class Meta:
    indexes = [
        models.Index(fields=['name', 'is_available']),
        models.Index(fields=['-created_at']),  # Сортировка
    ]
```

## Кэширование

### Кэширование запросов

```python
from django.core.cache import cache

def get_shaurma(slug):
    cache_key = f'shaurma_{slug}'
    shaurma = cache.get(cache_key)
    
    if shaurma is None:
        shaurma = Shaurma.objects.get(slug=slug)
        cache.set(cache_key, shaurma, 3600)  # 1 час
    
    return shaurma
```

### Кэширование в шаблонах

```jinja
{% cache 3600 shaurma.id %}
    {{ shaurma.description }}
{% endcache %}
```

## Оптимизация изображений

### ImageKit

Используйте ImageKit для автоматической обработки:

```python
thumbnail = ImageSpecField(
    source='picture',
    processors=[ResizeToFill(300, 200)],
    format='PNG',
    options={'quality': 90}
)
```

### Ленивая загрузка

```jinja
<img src="{{ shaurma.thumbnail.url }}" loading="lazy" alt="{{ shaurma.name }}">
```

## Пагинация

Используйте пагинацию для больших списков:

```python
from django.core.paginator import Paginator

def catalog(request):
    shaurmas = Shaurma.objects.filter(is_available=True)
    paginator = Paginator(shaurmas, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'main/catalog.jinja', {'page_obj': page_obj})
```

## Сжатие статических файлов

Используйте django-compressor:

```jinja
{% compress css %}
    <link rel="stylesheet" href="{% static 'main/css/style.css' %}">
{% endcompress %}
```

## Логирование производительности

```python
import time
import logging

logger = logging.getLogger('main')

def slow_view(request):
    start_time = time.time()
    # ... логика
    elapsed_time = time.time() - start_time
    logger.info(f'View took {elapsed_time:.2f}s')
```

## Профилирование

### Django Debug Toolbar

Активируйте в `.env`:

```
IS_DDT_ACTIVE=True
```

Показывает:

- SQL запросы и время выполнения
- Время рендеринга шаблонов
- Использование памяти

### cProfile

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Ваш код

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

## Лучшие практики

1. **Всегда используйте select_related/prefetch_related** для связанных объектов
2. **Добавляйте индексы** для часто используемых полей
3. **Используйте кэширование** для редко изменяемых данных
4. **Оптимизируйте изображения** через ImageKit
5. **Используйте пагинацию** для больших списков
6. **Сжимайте статические файлы** через django-compressor
7. **Профилируйте код** для поиска узких мест

