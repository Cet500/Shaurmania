# Стиль кода

## Python

Проект следует стандартам PEP 8 с некоторыми особенностями.

### Отступы и форматирование

- **Отступы:** 4 пробела (не табы)
- **Длина строки:** рекомендуется до 100 символов
- **Пустые строки:** 2 строки между классами, 1 между методами

### Именование

- **Классы:** `PascalCase`
  ```python
  class UserManager(BaseUserManager):
      pass
  ```

- **Функции/переменные:** `snake_case`
  ```python
  def create_user(self, name, email):
      user_name = name.lower()
  ```

- **Константы:** `UPPER_SNAKE_CASE`
  ```python
  MAX_AGE_REGISTRATION = 100
  MIN_AGE_REGISTRATION = 14
  ```

- **Приватные методы:** начинаются с `_`
  ```python
  def _validate_age(self, value):
      pass
  ```

### Импорты

Группируйте импорты в следующем порядке:

1. Стандартная библиотека
2. Сторонние библиотеки
3. Локальные импорты

```python
# Стандартная библиотека
from datetime import date
import os

# Сторонние библиотеки
from django.db import models
from imagekit.models import ImageSpecField

# Локальные импорты
from main.validators import validate_not_in_stop_words
from Shaurmania.settings import MIN_AGE_REGISTRATION
```

## Django

### Модели

- Используйте `verbose_name` для всех полей
- Группируйте связанные поля
- Используйте `related_name` для обратных связей
- Всегда указывайте `on_delete` для ForeignKey

**Пример:**

```python
class Shaurma(models.Model):
    # Основные поля
    name = models.CharField(
        max_length=60,
        unique=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=70,
        blank=True,
        verbose_name='URL-адрес'
    )
    
    # Связи
    category = models.ForeignKey(
        'ShaurmaCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shaurmas',
        verbose_name='Категория'
    )
    
    # Метаданные
    class Meta:
        verbose_name = 'шаурма'
        verbose_name_plural = 'шаурма'
        ordering = ['name']
        db_table = 'main_shaurma'
```

### Представления

- Используйте функциональные представления
- Группируйте по модулям в `views/`
- Используйте `get_object_or_404` для получения объектов
- Оптимизируйте запросы с `select_related` и `prefetch_related`

**Пример:**

```python
from django.shortcuts import render, get_object_or_404
from main.models import Shaurma

def product(request, slug):
    shaurma = get_object_or_404(
        Shaurma.objects.select_related('category'),
        slug=slug,
        is_available=True
    )
    return render(request, 'main/product.jinja', {'shaurma': shaurma})
```

### URL-маршруты

- Группируйте по функциональности
- Используйте именованные маршруты
- Комментируйте группы маршрутов

**Пример:**

```python
urlpatterns = [
    # CATALOG
    path('', v.index, name='index'),
    path('catalog', v.catalog, name='catalog'),
    path('product/<slug:slug>', v.product, name='product'),
    
    # AUTH
    path('login', v.login, name='login'),
    path('reg', v.reg, name='reg'),
]
```

## Шаблоны (Jinja2)

### Структура

- Используйте расширение `.jinja`
- Используйте наследование шаблонов
- Минимизируйте логику в шаблонах
- Группируйте логику в template tags

**Пример:**

```jinja
{% extends "base.jinja" %}

{% block title %}{{ shaurma.name }}{% endblock %}

{% block content %}
    <h1>{{ shaurma.name }}</h1>
    <p>{{ shaurma.description }}</p>
    
    {% if shaurma.images.exists() %}
        <div class="gallery">
            {% for image in shaurma.images.all() %}
                <img src="{{ image.thumbnail_md.url }}" alt="{{ image.caption }}">
            {% endfor %}
        </div>
    {% endif %}
{% endblock %}
```

### Template Tags

Создавайте кастомные template tags для сложной логики:

```python
# main/templatetags/functions.py
from django import template

register = template.Library()

@register.filter
def format_price(value):
    return f"{value} ₽"
```

Использование:

```jinja
{{ shaurma.price|format_price }}
```

## Комментарии

### Docstrings

Используйте docstrings для классов и функций:

```python
class UserManager(BaseUserManager):
    """Менеджер для модели User."""
    
    def create_user(self, name, email, username, password, **extra_fields):
        """
        Создает и сохраняет пользователя.
        
        Args:
            name: Имя пользователя
            email: Email адрес
            username: Логин
            password: Пароль
            **extra_fields: Дополнительные поля
        
        Returns:
            User: Созданный пользователь
        
        Raises:
            ValueError: Если обязательные поля не заполнены
        """
        if not name:
            raise ValueError('Введите имя')
        # ...
```

### Inline комментарии

Используйте комментарии для объяснения сложной логики:

```python
# Денормализация данных для оптимизации запросов
city = models.ForeignKey(
    'GeoCity',
    on_delete=models.PROTECT,
    editable=False  # Не редактируется вручную
)
```

## Обработка ошибок

### Валидация

Используйте кастомные валидаторы:

```python
from django.core.exceptions import ValidationError

def validate_age(value):
    """Валидация возраста пользователя."""
    today = date.today()
    min_age = today.replace(year=today.year - MIN_AGE_REGISTRATION)
    
    if value < min_age:
        raise ValidationError(
            f'Возраст должен быть не менее {MIN_AGE_REGISTRATION} лет.'
        )
```

### Исключения

Используйте специфичные исключения:

```python
# Плохо
raise Exception('Ошибка')

# Хорошо
raise ValueError('Имя не может быть пустым')
raise ValidationError('Некорректный формат email')
```
