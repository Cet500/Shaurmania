# Справка по URL

## Обзор

Проект использует модульную структуру URL, где каждое приложение имеет свой файл `urls.py`.

## Структура URL

```
/                          # Главный urls.py (Shaurmania/urls.py)
├── ''                     # main.urls
├── 'api/'                 # api.urls
├── 'cart/'                # cart.urls
└── 'admin-panel/'         # Django admin
```

## Основные URL (main)

### Главная страница и каталог

| URL               | Имя маршрута | Представление                | Описание               |
|-------------------|--------------|------------------------------|------------------------|
| `/`               | `index`      | `main.views.catalog.index`   | Главная страница       |
| `/catalog`        | `catalog`    | `main.views.catalog.catalog` | Каталог товаров        |
| `/product/<slug>` | `product`    | `main.views.catalog.product` | Страница товара (slug) |
| `/search`         | `search`     | `main.views.catalog.search`  | Поиск товаров          |

**Примеры:**

- `/` — главная страница
- `/catalog` — каталог
- `/product/klassicheskaya-shaurma` — страница товара

### Авторизация

| URL       | Имя маршрута | Представление            | Описание             |
|-----------|--------------|--------------------------|----------------------|
| `/login`  | `login`      | `main.views.auth.login`  | Страница входа       |
| `/reg`    | `reg`        | `main.views.auth.reg`    | Страница регистрации |
| `/logout` | `logout`     | `main.views.auth.logout` | Выход из системы     |

**Методы:**

- `GET /login` — отображение формы входа
- `POST /login` — обработка входа
- `GET /logout` — выход из системы

### Профили пользователей

| URL                | Имя маршрута  | Представление                    | Описание             |
|--------------------|---------------|----------------------------------|----------------------|
| `/user/<username>` | `user`        | `main.views.profile.user`        | Профиль пользователя |
| `/profile_closed`  | `user_closed` | `main.views.profile.user_closed` | Закрытый профиль     |

**Примеры:**

- `/user/admin` — профиль пользователя "admin"
- `/user/testuser` — профиль пользователя "testuser"

**Параметры:**

- `<username>` — строка, имя пользователя

### Локации доставки

| URL                | Имя маршрута | Представление                   | Описание            |
|--------------------|--------------|---------------------------------|---------------------|
| `/locations`       | `locations`  | `main.views.location.locations` | Список всех локаций |
| `/location/<slug>` | `location`   | `main.views.location.location`  | Страница локации    |

**Примеры:**

- `/locations` — список локаций
- `/location/moskva-centr` — конкретная локация

**Параметры:**

- `<slug>` — slug локации

### Новости

| URL                    | Имя маршрута  | Представление                 | Описание          |
|------------------------|---------------|-------------------------------|-------------------|
| `/news`                | `news`        | `main.views.news.news`        | Список новостей   |
| `/news/tag/<tag_slug>` | `news_by_tag` | `main.views.news.news`        | Новости по тегу   |
| `/news/<slug>`         | `news_detail` | `main.views.news.news_detail` | Детальная новость |

**Примеры:**

- `/news` — все новости
- `/news/tag/aktsii` — новости с тегом "aktsii"
- `/news/novaya-shaurma-v-menyu` — конкретная новость

**Параметры:**

- `<tag_slug>` — slug тега
- `<slug>` — slug новости

### Акции

| URL             | Имя маршрута | Представление             | Описание        |
|-----------------|--------------|---------------------------|-----------------|
| `/stocks`       | `stocks`     | `main.views.stock.stocks` | Список акций    |
| `/stock/<slug>` | `stock`      | `main.views.stock.stock`  | Детальная акция |

**Примеры:**

- `/stocks` — все акции
- `/stock/skidka-20` — конкретная акция

### О проекте

| URL         | Имя маршрута | Представление               | Описание         |
|-------------|--------------|-----------------------------|------------------|
| `/about`    | `about`      | `main.views.about.about`    | Страница "О нас" |
| `/feedback` | `feedback`   | `main.views.about.feedback` | Страница отзывов |

### Документация

| URL                    | Имя маршрута     | Представление                    | Описание                      |
|------------------------|------------------|----------------------------------|-------------------------------|
| `/docs`                | `docs`           | `main.views.docs.docs`           | Главная страница документации |
| `/docs/privacy_policy` | `privacy_policy` | `main.views.docs.privacy_policy` | Политика конфиденциальности   |
| `/docs/user_agreement` | `user_agreement` | `main.views.docs.user_agreement` | Пользовательское соглашение   |
| `/docs/user_consent`   | `user_consent`   | `main.views.docs.user_consent`   | Согласие пользователя         |
| `/docs/license`        | `license`        | `main.views.docs.license`        | Лицензия                      |
| `/docs/add_license_1`  | `add_license_1`  | `main.views.docs.add_license_1`  | Дополнительная лицензия 1     |
| `/docs/san_rules`      | `san_rules`      | `main.views.docs.san_rules`      | Санитарные правила            |
| `/docs/codex`          | `codex`          | `main.views.docs.codex`          | Кодекс                        |
| `/docs/decree`         | `decree`         | `main.views.docs.decree`         | Постановление                 |

## Корзина (cart)

| URL                         | Имя маршрута  | Представление            | Описание            | Методы |
|-----------------------------|---------------|--------------------------|---------------------|--------|
| `/cart/`                    | `cart`        | `cart.views.cart`        | Отображение корзины | GET    |
| `/cart/add/<shaurma_id>`    | `cart_add`    | `cart.views.cart_add`    | Добавление товара   | POST   |
| `/cart/remove/<shaurma_id>` | `cart_remove` | `cart.views.cart_remove` | Удаление товара     | POST   |

**Примеры:**

- `/cart/` — корзина
- `/cart/add/1` — добавить товар с ID=1
- `/cart/remove/1` — удалить товар с ID=1

**Параметры:**

- `<shaurma_id>` — целое число, ID товара

## API (api)

### Административные эндпоинты

| URL                           | Имя маршрута             | Представление                      | Описание         | Аутентификация    |
|-------------------------------|--------------------------|------------------------------------|------------------|-------------------|
| `/api/admin/factories`        | `admin_factories`        | `api.views.admin_factories`        | Список фабрик    | Суперпользователь |
| `/api/admin/factories/<name>` | `admin_factory_generate` | `api.views.admin_factory_generate` | Генерация данных | Суперпользователь |

**Примеры:**

- `/api/admin/factories` — список доступных фабрик
- `/api/admin/factories/shaurma?count=5` — сгенерировать 5 товаров

**Параметры:**

- `<name>` — название фабрики (shaurma, user, location и т.д.)
- `count` (query) — количество объектов (1-50)

### Публичные эндпоинты

| URL                  | Имя маршрута | Представление        | Описание                 |
|----------------------|--------------|----------------------|--------------------------|
| `/api/geo_code/<ip>` | `geo_code`   | `api.views.geo_code` | Определение страны по IP |

**Примеры:**

- `/api/geo_code/8.8.8.8` — определить страну для IP 8.8.8.8

**Параметры:**

- `<ip>` — IPv4 адрес

## Админ-панель

| URL             | Имя маршрута | Описание            |
|-----------------|--------------|---------------------|
| `/admin-panel/` | -            | Django админ-панель |

**Требования:**

- Аутентификация
- Права `is_staff=True` или `is_superuser=True`

## Обработка ошибок

| URL            | Имя маршрута | Представление                 | Описание                  |
|----------------|--------------|-------------------------------|---------------------------|
| `/errors/400/` | `errors_400` | `main.views.errors.error_400` | Ошибка 400 (Bad Request)  |
| `/errors/403/` | `errors_403` | `main.views.errors.error_403` | Ошибка 403 (Forbidden)    |
| `/errors/404/` | `errors_404` | `main.views.errors.error_404` | Ошибка 404 (Not Found)    |
| `/errors/500/` | `errors_500` | `main.views.errors.error_500` | Ошибка 500 (Server Error) |

**Обработчики:**

- `handler400` — автоматически вызывается при ошибке 400
- `handler403` — автоматически вызывается при ошибке 403
- `handler404` — автоматически вызывается при ошибке 404
- `handler500` — автоматически вызывается при ошибке 500

## Использование в коде

### В Python

```python
from django.urls import reverse
from django.shortcuts import redirect

# Получить URL по имени
url = reverse('product', args=['klassicheskaya-shaurma'])
# Результат: '/product/klassicheskaya-shaurma'

# Редирект
return redirect('catalog')

# Редирект с параметрами
return redirect('product', slug='klassicheskaya-shaurma')
```

### В шаблонах Jinja2

```jinja
{# Генерация URL #}
<a href="{{ url('product', slug='klassicheskaya-shaurma') }}">Товар</a>

{# С переменной #}
<a href="{{ url('product', slug=shaurma.slug) }}">{{ shaurma.name }}</a>

{# Редирект в форме #}
<form action="{{ url('cart_add', shaurma_id=shaurma.id) }}" method="post">
    {% csrf_token %}
    <button type="submit">Добавить в корзину</button>
</form>
```

## Типы параметров

### str

Строка (по умолчанию):

```python
path('user/<str:username>', views.user, name='user')
```

### int

Целое число:

```python
path('cart/add/<int:shaurma_id>', views.cart_add, name='cart_add')
```

### slug

Slug (латиница, цифры, дефисы, подчеркивания):

```python
path('product/<slug:slug>', views.product, name='product')
```

### uuid

UUID:

```python
path('promocode/<uuid:code_uuid>', views.promocode, name='promocode')
```

## Query параметры

Некоторые представления поддерживают query параметры:

```python
# Поиск
/search?q=шаурма

# Каталог с фильтрами
/catalog?category=klassicheskaya&price_min=200&price_max=500

# Новости с пагинацией
/news?page=2

# API с параметрами
/api/admin/factories/shaurma?count=10
```

## Лучшие практики

1. **Используйте именованные маршруты** — всегда указывайте `name` в `path()`
2. **Группируйте URL** — используйте комментарии для группировки
3. **Используйте slug** — для читаемых URL вместо ID
4. **Валидируйте параметры** — проверяйте параметры в представлениях
5. **Используйте reverse()** — вместо хардкода URL в коде

