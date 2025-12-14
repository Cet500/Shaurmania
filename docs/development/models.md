# Работа с моделями

## Создание новой модели

### Шаги

1. **Создайте файл модели** в соответствующем приложении
   ```python
   # main/models/example.py
   from django.db import models
   ```

2. **Определите поля** с валидацией и verbose_name
   ```python
   class Example(models.Model):
       name = models.CharField(
           max_length=100,
           verbose_name='Название'
       )
   ```

3. **Добавьте методы** `__str__` и `save` (если нужно)
   ```python
   def __str__(self):
       return self.name
   
   def save(self, *args, **kwargs):
       # Кастомная логика сохранения
       super().save(*args, **kwargs)
   ```

4. **Зарегистрируйте в admin.py**
   ```python
   # main/admin/example.py
   from django.contrib import admin
   from main.models import Example
   
   @admin.register(Example)
   class ExampleAdmin(admin.ModelAdmin):
       list_display = ['name', 'created_at']
   ```

5. **Создайте миграцию**
   ```bash
   python manage.py makemigrations
   ```

6. **Примените миграцию**
   ```bash
   python manage.py migrate
   ```

## Работа с изображениями

### ImageKit

Используйте `django-imagekit` для автоматической обработки изображений:

```python
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Shaurma(models.Model):
    picture = models.ImageField(upload_to='shaurma_images')
    
    # Средняя миниатюра
    thumbnail_md = ImageSpecField(
        source='picture',
        processors=[ResizeToFill(640, 450)],
        format='PNG',
        options={'quality': 90}
    )
    
    # Маленькая миниатюра
    thumbnail_sm = ImageSpecField(
        source='picture',
        processors=[ResizeToFill(285, 200)],
        format='PNG',
        options={'quality': 90}
    )
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.picture:
            self.thumbnail_md.generate()
            self.thumbnail_sm.generate()
```

### Валидация изображений

```python
from django.core.validators import FileExtensionValidator

class UserAvatar(models.Model):
    avatar = models.ImageField(
        upload_to='user_avatars',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
```

## Валидация данных

### Кастомные валидаторы

Создавайте валидаторы в `validators.py`:

```python
# main/validators.py
from django.core.exceptions import ValidationError
from lists.stop_words import STOP_WORDS

def validate_not_in_stop_words(value):
    """Проверка на стоп-слова."""
    if value.lower() in STOP_WORDS:
        raise ValidationError('Это слово запрещено')
```

Использование в модели:

```python
from main.validators import validate_not_in_stop_words

class User(models.Model):
    name = models.CharField(
        max_length=40,
        validators=[validate_not_in_stop_words],
        verbose_name='Имя'
    )
```

### Валидация в методе clean

```python
class User(models.Model):
    date_of_birth = models.DateField()
    
    def clean(self):
        from django.core.exceptions import ValidationError
        from Shaurmania.settings import MIN_AGE_REGISTRATION
        
        if self.date_of_birth:
            today = date.today()
            min_age = today.replace(year=today.year - MIN_AGE_REGISTRATION)
            if self.date_of_birth > min_age:
                raise ValidationError({
                    'date_of_birth': f'Возраст должен быть не менее {MIN_AGE_REGISTRATION} лет.'
                })
```

## Связи между моделями

### ForeignKey

```python
class Shaurma(models.Model):
    category = models.ForeignKey(
        'ShaurmaCategory',
        on_delete=models.SET_NULL,  # Всегда указывайте on_delete
        null=True,
        blank=True,
        related_name='shaurmas',  # Имя для обратной связи
        verbose_name='Категория'
    )
```

**Варианты on_delete:**

- `CASCADE` — удалить связанные объекты
- `PROTECT` — запретить удаление
- `SET_NULL` — установить NULL (нужен null=True)
- `SET_DEFAULT` — установить значение по умолчанию
- `DO_NOTHING` — ничего не делать

### ManyToManyField

```python
class News(models.Model):
    tags = models.ManyToManyField(
        'NewsTag',
        blank=True,
        related_name='news',
        verbose_name='Теги'
    )
```

### OneToOneField

```python
class Address(models.Model):
    base_address = models.OneToOneField(
        'BaseAddress',
        on_delete=models.CASCADE,
        related_name='address'
    )
```

## Методы моделей

### __str__

Всегда определяйте `__str__` для удобного отображения:

```python
def __str__(self):
    return f'{self.name} | {self.email}'
```

### save

Переопределяйте `save` для автоматической обработки:

```python
def save(self, *args, **kwargs):
    # Генерация slug
    if not self.slug:
        self.slug = slugify(self.name)
    
    # Автоматический расчет даты окончания
    if not self.id:
        self.date_end = self.date_add + timedelta(days=self.duration)
    
    super().save(*args, **kwargs)
```

### Свойства (properties)

Используйте `@property` для вычисляемых значений:

```python
@property
def avatar_48_url(self):
    avatar = self.avatars.filter(is_primary=True).first()
    if avatar and avatar.avatar:
        return avatar.avatar_48x.url
    return static('main/img/avatar/avatar_015.png')
```

## Meta класс

Всегда определяйте `Meta` класс:

```python
class Meta:
    verbose_name = 'шаурма'
    verbose_name_plural = 'шаурма'
    ordering = ['name']  # Сортировка по умолчанию
    db_table = 'main_shaurma'  # Имя таблицы (опционально)
    indexes = [
        models.Index(fields=['name', 'is_available']),
    ]  # Индексы для оптимизации
```

## QuerySet методы

### Фильтрация

```python
# Доступные товары
shaurmas = Shaurma.objects.filter(is_available=True)

# Несколько условий
shaurmas = Shaurma.objects.filter(
    is_available=True,
    price__gte=200,
    price__lte=500
)

# Исключение
shaurmas = Shaurma.objects.exclude(is_available=False)
```

### Оптимизация запросов

```python
# select_related для ForeignKey
shaurmas = Shaurma.objects.select_related('category').all()

# prefetch_related для ManyToMany и обратных ForeignKey
news = News.objects.prefetch_related('tags').all()

# Комбинация
shaurmas = Shaurma.objects.select_related('category').prefetch_related('images').all()
```

### Агрегация

```python
from django.db.models import Avg, Count, Sum

# Средняя цена
avg_price = Shaurma.objects.aggregate(Avg('price'))

# Количество товаров в категории
categories = ShaurmaCategory.objects.annotate(
    shaurma_count=Count('shaurmas')
)
```

## Миграции

### Создание миграции

```bash
python manage.py makemigrations
```

### Применение миграции

```bash
python manage.py migrate
```

### Откат миграции

```bash
python manage.py migrate app_name migration_number
```

### Просмотр миграций

```bash
python manage.py showmigrations
```

## Лучшие практики

1. **Всегда используйте verbose_name** для полей
2. **Указывайте on_delete** для всех ForeignKey
3. **Используйте related_name** для обратных связей
4. **Определяйте __str__** для всех моделей
5. **Добавляйте индексы** для часто используемых полей
6. **Используйте select_related/prefetch_related** для оптимизации
7. **Валидируйте данные** на уровне модели
8. **Группируйте поля** логически в модели

