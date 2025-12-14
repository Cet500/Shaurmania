# Cookbook — Готовые примеры

## Создание моделей

### Базовая модель

```python
from django.db import models

class Example(models.Model):
    name        = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'пример'
        verbose_name_plural = 'примеры'
        ordering = ['-created_at']
```

### Модель с ForeignKey

```python
from django.db import models


class Category( models.Model ):
	name = models.CharField( max_length = 60, verbose_name = 'Название' )

	def __str__( self ):
		return self.name


class Item( models.Model ):
	name = models.CharField( max_length = 100, verbose_name = 'Название' )
	category = models.ForeignKey(
		Category,
		on_delete = models.CASCADE,
		related_name = 'items',
		verbose_name = 'Категория'
	)
	price = models.PositiveSmallIntegerField( verbose_name = 'Цена' )

	def __str__( self ):
		return f'{self.category.name} - {self.name}'
```

### Модель с изображениями

```python
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    picture = models.ImageField(upload_to='products', verbose_name='Изображение')
    
    # Миниатюра
    thumbnail = ImageSpecField(
        source='picture',
        processors=[ResizeToFill(300, 200)],
        format='PNG',
        options={'quality': 90}
    )
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.picture:
            self.thumbnail.generate()
```

### Модель с валидацией

```python
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    price = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        verbose_name='Цена'
    )
    
    def clean(self):
        if self.price < 0:
            raise ValidationError({'price': 'Цена не может быть отрицательной'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
```

### Модель с автоматическим slug

```python
from django.db import models
from slugify import slugify

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=220, blank=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержание')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
```

## Создание представлений

### Простое представление

```python
from django.shortcuts import render
from main.models import Shaurma

def catalog(request):
    shaurmas = Shaurma.objects.filter(is_available=True)
    return render(request, 'main/catalog.jinja', {'shaurmas': shaurmas})
```

### Представление с параметром

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

### Представление с формой (GET)

```python
from django.shortcuts import render
from django.db.models import Q
from main.models import Shaurma

def search(request):
    query = request.GET.get('q', '')
    shaurmas = Shaurma.objects.filter(is_available=True)
    
    if query:
        shaurmas = shaurmas.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    return render(request, 'main/search.jinja', {
        'shaurmas': shaurmas,
        'query': query
    })
```

### Представление с формой (POST)

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from main.forms import ShaurmaForm

def create_shaurma(request):
    if request.method == 'POST':
        form = ShaurmaForm(request.POST, request.FILES)
        if form.is_valid():
            shaurma = form.save()
            messages.success(request, 'Товар успешно создан')
            return redirect('product', slug=shaurma.slug)
    else:
        form = ShaurmaForm()
    
    return render(request, 'main/create_shaurma.jinja', {'form': form})
```

### Представление с авторизацией

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile(request):
    return render(request, 'main/profile.jinja', {
        'user': request.user
    })
```

### Представление с пагинацией

```python
from django.core.paginator import Paginator
from django.shortcuts import render
from main.models import Shaurma

def catalog(request):
    shaurmas = Shaurma.objects.filter(is_available=True)
    paginator = Paginator(shaurmas, 20)  # 20 на страницу
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'main/catalog.jinja', {'page_obj': page_obj})
```

## Создание форм

### ModelForm

```python
from django import forms
from main.models import Shaurma

class ShaurmaForm(forms.ModelForm):
    class Meta:
        model = Shaurma
        fields = ['name', 'category', 'price', 'description', 'picture']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'min': 1,
                'step': 1
            })
        }
```

### Форма с валидацией

```python
from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Имя')
    email = forms.EmailField(label='Email')
    message = forms.CharField(widget=forms.Textarea, label='Сообщение')
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise ValidationError('Имя слишком короткое')
        return name
    
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise ValidationError('Сообщение слишком короткое')
        return message
```

## Работа с QuerySet

### Базовые запросы

```python
from main.models import Shaurma


# Все товары
all_shaurmas = Shaurma.objects.all()

# Доступные товары
available = Shaurma.objects.filter( is_available = True )

# Товары дороже 200 рублей
expensive = Shaurma.objects.filter( price__gte = 200 )

# Товары в диапазоне цен
range_price = Shaurma.objects.filter( price__gte = 200, price__lte = 500 )

# Поиск по названию
search = Shaurma.objects.filter( name__icontains = 'классическая' )

# Сортировка
sorted_shaurmas = Shaurma.objects.order_by( '-price' )
```

### Оптимизация запросов

```python
# select_related для ForeignKey
shaurmas = Shaurma.objects.select_related( 'category' ).all()

# prefetch_related для ManyToMany
news = News.objects.prefetch_related( 'tags' ).all()

# Комбинация
shaurmas = Shaurma.objects.select_related( 'category' ).prefetch_related( 'images' ).all()

# only() для загрузки только нужных полей
users = User.objects.only( 'username', 'email' ).all()
```

### Агрегация

```python
from django.db.models import Avg, Count, Sum, Max, Min


# Средняя цена
avg_price = Shaurma.objects.aggregate( Avg( 'price' ) )

# Количество товаров в категории
categories = ShaurmaCategory.objects.annotate(
	shaurma_count = Count( 'shaurmas' )
)

# Сумма всех цен
total = Shaurma.objects.aggregate( Sum( 'price' ) )
```

## Работа с шаблонами

### Базовый шаблон

```jinja
{# base.jinja #}
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Shaurmania{% endblock %}</title>
</head>
<body>
    <header>
        {% block header %}{% endblock %}
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        {% block footer %}{% endblock %}
    </footer>
</body>
</html>
```

### Наследование шаблона

```jinja
{# product.jinja #}
{% extends "base.jinja" %}

{% block title %}{{ shaurma.name }} - Shaurmania{% endblock %}

{% block content %}
    <h1>{{ shaurma.name }}</h1>
    <p>{{ shaurma.description }}</p>
    <p>Цена: {{ shaurma.price }} ₽</p>
{% endblock %}
```

### Циклы и условия

```jinja
{% if shaurmas %}
    <ul>
        {% for shaurma in shaurmas %}
            <li>
                <a href="{{ url('product', slug=shaurma.slug) }}">
                    {{ shaurma.name }}
                </a>
                - {{ shaurma.price }} ₽
            </li>
        {% endfor %}
    </ul>
{% else %}
    <p>Товары не найдены</p>
{% endif %}
```

### Фильтры

```jinja
{# Форматирование даты #}
{{ shaurma.created_at|date:"d.m.Y" }}

{# Форматирование числа #}
{{ shaurma.price|floatformat:2 }}

{# Обрезка текста #}
{{ shaurma.description|truncatewords:20 }}

{# Значение по умолчанию #}
{{ shaurma.short_text|default:"Нет описания" }}

{# Первая буква заглавная #}
{{ shaurma.name|title }}
```

### Включение частичных шаблонов

```jinja
{# Включение шапки #}
{% include "partials/header.jinja" %}

{# С переменными #}
{% include "partials/product_card.jinja" with shaurma=item %}
```

## Работа с админ-панелью

### Базовая регистрация

```python
from django.contrib import admin
from main.models import Shaurma

@admin.register(Shaurma)
class ShaurmaAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_available', 'created_at']
    list_filter = ['is_available', 'category', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
```

### Расширенная регистрация

```python
@admin.register(Shaurma)
class ShaurmaAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'created_at']
    list_filter = ['is_available', 'category', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    list_per_page = 25
    
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'slug', 'category')
        }),
        ('Описание', {
            'fields': ('description', 'compound')
        }),
        ('Цена и доступность', {
            'fields': ('price', 'weight', 'is_available')
        }),
    )
    
    readonly_fields = ['slug', 'created_at', 'updated_at']
```

## Тестирование

### Тест модели

```python
import pytest
from main.models import User

@pytest.mark.django_db
def test_user_creation():
    user = User.objects.create_user(
        name='Test',
        email='test@example.com',
        username='testuser',
        password='testpass123'
    )
    assert user.username == 'testuser'
    assert user.is_active is True
```

### Тест представления

```python
import pytest
from django.urls import reverse
from main.models import Shaurma

@pytest.mark.django_db
def test_catalog_view(client):
    Shaurma.objects.create(
        name='Test Shaurma',
        price=250,
        weight=300,
        compound='Test'
    )
    
    response = client.get(reverse('catalog'))
    assert response.status_code == 200
    assert 'Test Shaurma' in response.content.decode()
```

### Тест с Factory Boy

```python
import pytest
from main.factories import ShaurmaFactory

@pytest.mark.django_db
def test_with_factory():
    shaurma = ShaurmaFactory()
    assert shaurma.price > 0
    assert shaurma.is_available is True
```

## Работа с сессиями

### Сохранение в сессии

```python
def add_to_cart(request, shaurma_id):
    cart = request.session.get('cart', [])
    cart.append(shaurma_id)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')
```

### Получение из сессии

```python
def get_cart(request):
    cart = request.session.get('cart', [])
    return cart
```

## Логирование

### Базовое логирование

```python
import logging

logger = logging.getLogger('main')

def my_view(request):
    logger.info('Пользователь зашел на страницу')
    try:
        # Код
        pass
    except Exception as e:
        logger.error('Произошла ошибка', exc_info=True)
```

### Логирование с контекстом

```python
import logging

logger = logging.getLogger('main')

def add_to_cart(request, shaurma_id):
    logger.info(
        'Добавление товара в корзину',
        extra={
            'user_id': request.user.id,
            'shaurma_id': shaurma_id
        }
    )
```

## Работа с изображениями

### Загрузка изображения

```python
def upload_image(request):
    if request.method == 'POST' and request.FILES:
        image = request.FILES['image']
        # Сохранение через модель
        shaurma = Shaurma.objects.get(id=1)
        shaurma.picture = image
        shaurma.save()
```

### Отображение в шаблоне

```jinja
{# Основное изображение #}
<img src="{{ shaurma.picture.url }}" alt="{{ shaurma.name }}">

{# Миниатюра #}
<img src="{{ shaurma.thumbnail_sm.url }}" alt="{{ shaurma.name }}">

{# С проверкой наличия #}
{% if shaurma.picture %}
    <img src="{{ shaurma.picture.url }}" alt="{{ shaurma.name }}">
{% endif %}
```

## Работа с корзиной

### Добавление в корзину (авторизованный)

```python
from cart.models import Cart

def add_to_cart(request, shaurma_id):
    if request.user.is_authenticated:
        shaurma = get_object_or_404(Shaurma, id=shaurma_id)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            item=shaurma,
            defaults={'quanity': 1}
        )
        if not created:
            cart_item.quanity += 1
            cart_item.save()
    return redirect('cart')
```

### Добавление в корзину (анонимный)

```python
def add_to_cart(request, shaurma_id):
    if not request.user.is_authenticated:
        cart_data = request.session.get('cart_items', {})
        cart_data[str(shaurma_id)] = cart_data.get(str(shaurma_id), 0) + 1
        request.session['cart_items'] = cart_data
        request.session.modified = True
    return redirect('cart')
```

## Полезные паттерны

### Контекстный процессор

```python
# main/context_processors.py
def feature_flags(request):
    from django.conf import settings
    return {
        'IS_HALLOWEEN': settings.IS_HALLOWEEN,
        'IS_NEW_YEAR': settings.IS_NEW_YEAR,
    }
```

Использование в шаблоне:

```jinja
{% if IS_HALLOWEEN %}
    {# Хэллоуинская тема #}
{% endif %}
```

### Template Tag

```python
# main/templatetags/functions.py
from django import template

register = template.Library()

@register.filter
def format_price(value):
    return f"{value} ₽"

@register.simple_tag
def get_total_price(items):
    return sum(item.price for item in items)
```

Использование:

```jinja
{{ shaurma.price|format_price }}
{% get_total_price shaurmas as total %}
```

