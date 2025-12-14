# Отладка

## Django Debug Toolbar

### Активация

В `.env`:

```
IS_DDT_ACTIVE=True
```

### Возможности

- SQL запросы и время выполнения
- Время рендеринга шаблонов
- Переменные шаблона
- Статические файлы
- Использование памяти

## Логирование

### Настройка логгеров

```python
import logging

logger = logging.getLogger('main')
logger.info('Информационное сообщение')
logger.warning('Предупреждение')
logger.error('Ошибка', exc_info=True)
```

### Уровни логирования

- `DEBUG` — детальная информация для отладки
- `INFO` — общая информация
- `WARNING` — предупреждения
- `ERROR` — ошибки
- `CRITICAL` — критические ошибки

### Логирование SQL

В настройках Django:

```python
LOGGING = {
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        }
    }
}
```

## Отладчик pdb

### Использование

```python
import pdb

def my_view(request):
    pdb.set_trace()  # Точка остановки
    # Код после этой строки будет выполняться пошагово
    shaurma = Shaurma.objects.get(slug=slug)
    return render(request, 'main/product.jinja', {'shaurma': shaurma})
```

### Команды pdb

- `n` (next) — следующая строка
- `s` (step) — войти в функцию
- `c` (continue) — продолжить выполнение
- `l` (list) — показать код
- `p variable` — вывести значение переменной
- `q` (quit) — выйти

## IPython

### Установка

```bash
pip install ipython
```

### Использование

```python
from IPython import embed

def my_view(request):
    embed()  # Интерактивная консоль
    # ...
```

## Проверка запросов

### Логирование SQL

```python
from django.db import connection

def my_view(request):
    # Ваш код
    queries = connection.queries
    print(f'Количество запросов: {len(queries)}')
    for query in queries:
        print(query['sql'])
```

### explain()

```python
shaurmas = Shaurma.objects.filter(is_available=True)
print(shaurmas.explain())
```

## Проверка шаблонов

### Отладка переменных

В шаблоне:

```jinja
{{ debug() }}  # Показать все переменные
```

### Логирование в шаблонах

```jinja
{% set _ = logger.info('Значение: ' + variable) %}
```

## Обработка ошибок

### try/except с логированием

```python
import logging

logger = logging.getLogger('main')

try:
    shaurma = Shaurma.objects.get(slug=slug)
except Shaurma.DoesNotExist:
    logger.error(f'Шаурма не найдена: {slug}', exc_info=True)
    return HttpResponseNotFound()
```

### Sentry (для продакшена)

```python
# settings.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

## Проверка производительности

### timeit

```python
import timeit

def test_function():
    # Ваш код

time = timeit.timeit(test_function, number=1000)
print(f'Время выполнения: {time:.4f}s')
```

### memory_profiler

```python
from memory_profiler import profile

@profile
def my_function():
    # Ваш код
```

## Проверка валидации

### full_clean()

```python
shaurma = Shaurma(name='Test', price=250)
try:
    shaurma.full_clean()
except ValidationError as e:
    print(e.message_dict)
```

## Лучшие практики

1. **Используйте Django Debug Toolbar** для разработки
2. **Логируйте важные события** с правильным уровнем
3. **Используйте pdb** для пошаговой отладки
4. **Проверяйте SQL запросы** на оптимизацию
5. **Обрабатывайте исключения** с логированием
6. **Используйте профилирование** для поиска узких мест
7. **Тестируйте на реальных данных** перед продакшеном

