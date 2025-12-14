# Представления приложения `main`

## Обзор

Приложение `main` использует функциональные представления, организованные по модулям в директории `main/views/`.

## Структура views

```
main/views/
├── __init__.py        # Экспорт всех представлений
├── about.py           # Страница "О нас"
├── auth.py            # Авторизация
├── catalog.py         # Каталог товаров
├── docs.py            # Документация
├── errors.py          # Обработка ошибок
├── location.py        # Локации доставки
├── news.py            # Новости
├── profile.py         # Профили пользователей
└── stock.py           # Акции
```

## URL-маршруты

### Основные страницы

| URL               | Представление | Модуль       | Описание         |
|-------------------|---------------|--------------|------------------|
| `/`               | `index`       | `catalog.py` | Главная страница |
| `/catalog`        | `catalog`     | `catalog.py` | Каталог товаров  |
| `/product/<slug>` | `product`     | `catalog.py` | Страница товара  |
| `/search`         | `search`      | `catalog.py` | Поиск            |

### Авторизация

| URL       | Представление | Модуль    | Описание    |
|-----------|---------------|-----------|-------------|
| `/login`  | `login`       | `auth.py` | Вход        |
| `/reg`    | `reg`         | `auth.py` | Регистрация |
| `/logout` | `logout`      | `auth.py` | Выход       |

### Профили

| URL                | Представление | Модуль       | Описание             |
|--------------------|---------------|--------------|----------------------|
| `/user/<username>` | `user`        | `profile.py` | Профиль пользователя |
| `/profile_closed`  | `user_closed` | `profile.py` | Закрытый профиль     |

### Локации

| URL                | Представление | Модуль        | Описание         |
|--------------------|---------------|---------------|------------------|
| `/locations`       | `locations`   | `location.py` | Список локаций   |
| `/location/<slug>` | `location`    | `location.py` | Страница локации |

### Новости

| URL                    | Представление | Модуль    | Описание          |
|------------------------|---------------|-----------|-------------------|
| `/news`                | `news`        | `news.py` | Список новостей   |
| `/news/tag/<tag_slug>` | `news`        | `news.py` | Новости по тегу   |
| `/news/<slug>`         | `news_detail` | `news.py` | Детальная новость |

### Акции

| URL             | Представление | Модуль     | Описание        |
|-----------------|---------------|------------|-----------------|
| `/stocks`       | `stocks`      | `stock.py` | Список акций    |
| `/stock/<slug>` | `stock`       | `stock.py` | Детальная акция |

### О проекте

| URL         | Представление | Модуль     | Описание |
|-------------|---------------|------------|----------|
| `/about`    | `about`       | `about.py` | О нас    |
| `/feedback` | `feedback`    | `about.py` | Отзывы   |

### Документация

| URL                    | Представление    | Модуль    | Описание                    |
|------------------------|------------------|-----------|-----------------------------|
| `/docs`                | `docs`           | `docs.py` | Документация                |
| `/docs/privacy_policy` | `privacy_policy` | `docs.py` | Политика конфиденциальности |
| `/docs/user_agreement` | `user_agreement` | `docs.py` | Пользовательское соглашение |
| `/docs/user_consent`   | `user_consent`   | `docs.py` | Согласие пользователя       |
| `/docs/license`        | `license`        | `docs.py` | Лицензия                    |
| `/docs/add_license_1`  | `add_license_1`  | `docs.py` | Дополнительная лицензия 1   |
| `/docs/san_rules`      | `san_rules`      | `docs.py` | Санитарные правила          |
| `/docs/codex`          | `codex`          | `docs.py` | Кодекс                      |
| `/docs/decree`         | `decree`         | `docs.py` | Постановление               |

### Обработка ошибок

| URL            | Представление | Модуль      | Описание   |
|----------------|---------------|-------------|------------|
| `/errors/400/` | `error_400`   | `errors.py` | Ошибка 400 |
| `/errors/403/` | `error_403`   | `errors.py` | Ошибка 403 |
| `/errors/404/` | `error_404`   | `errors.py` | Ошибка 404 |
| `/errors/500/` | `error_500`   | `errors.py` | Ошибка 500 |

## Примеры представлений

### Каталог товаров

```python
# main/views/catalog.py
from django.shortcuts import render
from main.models import Shaurma

def catalog(request):
    shaurmas = Shaurma.objects.filter(is_available=True).select_related('category')
    return render(request, 'main/catalog.jinja', {'shaurmas': shaurmas})
```

### Страница товара

```python
# main/views/catalog.py
from django.shortcuts import render, get_object_or_404
from main.models import Shaurma

def product(request, slug):
    shaurma = get_object_or_404(
        Shaurma,
        slug=slug,
        is_available=True
    )
    return render(request, 'main/product.jinja', {'shaurma': shaurma})
```

### Авторизация

```python
# main/views/auth.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'main/login.jinja')
```

## Оптимизация запросов

Представления используют оптимизацию запросов:

- `select_related()` для ForeignKey связей
- `prefetch_related()` для ManyToMany и обратных ForeignKey
- Фильтрация доступных товаров через `is_available=True`

