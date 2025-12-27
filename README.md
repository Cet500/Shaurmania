# ШаурМания

Сайт по продаже шаурмы с доставкой на Django.


## 📋 Описание

ШаурМания — это веб-приложение для заказа шаурмы с доставкой.
Проект включает систему управления товарами, корзину покупок, 
промокоды, достижения, локации доставки и систему отзывов.

Это проект, который до сих пор находится в стадии разработки,
но очень стремится стать большим и сильным сайтом.

![data-version](https://img.shields.io/badge/data_version-10-4c1?style=for-the-badge)

> ⚠️ Переход с 7 до 10 версии требует полного пересоздания базы данных. 


## ✨ Основные возможности

* 🍽 Каталог шаурмы с категориями
* 🛒 Корзина покупок
* 📍 Локации доставки
* 🎁 Система промокодов со скидками
* 🏆 Достижения пользователей
* ⭐ Система отзывов
* 📸 Галерея изображений товаров
* 🎨 Адаптивные шаблоны
* 📊 Админ-панель Django


## 🛠 Технологический стек

| Часть сайта               | Технология                  |
|---------------------------|-----------------------------|
| **Backend**               | Django 6.0                  |
| **База данных**           | SQLite3                     |
| **Шаблоны**               | Jinja2 (через django-jinja) |
| **Обработка изображений** | django-imagekit             |
| **Сжатие статики**        | django-compressor           |
| **Тестирование**          | pytest, pytest-django       |


## 📦 Требования

- Python 3.13+
- venv
- UV (менеджер пакетов)
- SQLite


## 🚀 Установка и настройка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Cet500/Shaurmania
   cd Shaurmania
   ```

2. **Создайте виртуальное окружение**
   ```bash
   uv venv
   
   # Если UV нет
   
   # Windows
   python -m venv .venv
   # Linux/Mac
   python3 -m venv .venv
   ```

3. **Установите зависимости через UV:**
   ```
   # Windows
   source .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   
   # Если UV нет
   pip install uv
   
   uv sync
   ```

4. **Создайте файл `.env` в корне проекта согласно файлу `.env.example`**

5. **Примените миграции:**
   ```bash
   python manage.py migrate
   ```

6. **Загрузите тестовые данные (раздел управление данными)**

7. **Создайте суперпользователя:**
   ```bash
   python manage.py createsuperuser
   ```


## ▶ Запуск проекта

1. **Сервер разработки:**
   ```bash
   python manage.py runserver
   ```

2. **Пробный запуск ( Windows ):**
   ```bash
   waitress-serve --host=0.0.0.0 --port=8000 --threads=8 --backlog=2048 Shaurmania.wsgi:application
   ```
   
3. **Боевой запуск ( Linux ):**
   ```bash
   gunicorn --bind 0.0.0.0:8000 --workers 16 --worker-class gevent Shaurmania.wsgi:application
   ```
   
 - Приложение будет доступно по адресу:
   ```url
   http://127.0.0.1:8000
   ```
   
 - Админ-панель:
   ```url
   http://127.0.0.1:8000/admin-panel/
   ```

**Примечание:**

Реальный запуск стоит производить только под Linux на связке
Django+Gunicorn+Nginx.


## 🧪 Тестирование

1. Запуск тестов через Django:
   ```bash
   python manage.py test
   ```

2. Запуск тестов с помощью pytest:
   ```bash
   pytest -v
   ```

3. С покрытием кода:
   ```bash
   python manage.py coverage
   ```


## 📁 Структура проекта

```
Shaurmania/
├── api/               # Приложение API
├── cart/              # Приложение корзины (корзина, заказы, промокоды)
├── ext_database       # Внешние используемые базы данных
├── geodata/           # Приложение предоставления геоданных
├── lists/             # Разные списки
├── logs/              # Логи приложения
├── main/              # Основное приложение (товары, пользователи, отзывы, локации)
├── media/             # Загружаемые файлы (изображения товаров, аватары)
├── security/          # Приложение безопасности
├── Shaurmania/        # Настройки проекта
├── static/            # Статические файлы (CSS, JS, изображения)
├── template/          # Шаблоны Jinja2
├── .env               # Настройки окружения (создаётся уникально)
├── .env.example       # Пример настроек окружения
├── .gitigone          # Запрещённые для коммита файлы
├── manage.py          # Django management script
├── README.md          # Этот файл
└── requirements.txt   # Требуемые python-пакеты
```


## 💾 Управление данными

### Сохранение данных

```bash
   python -Xutf8 manage.py dumpdata main.ShaurmaCategory -o main/fixtures/shaurma_categories.json
   python -Xutf8 manage.py dumpdata main.Shaurma -o main/fixtures/shaurma.json
   python -Xutf8 manage.py dumpdata main.Review -o main/fixtures/reviews.json
   python -Xutf8 manage.py dumpdata main.Location -o main/fixtures/locations.json
   python -Xutf8 manage.py dumpdata main.Achievement -o main/fixtures/achievements.json
   python -Xutf8 manage.py dumpdata main.Stock -o main/fixtures/stocks.json
   python -Xutf8 manage.py dumpdata cart.Promocode -o cart/fixtures/promocodes.json
   python -Xutf8 manage.py dumpdata main.ShaurmaImage -o main/fixtures/shaurma_images.json
   python -Xutf8 manage.py dumpdata main.NewsTag -o main/fixtures/news_tags.json
   python -Xutf8 manage.py dumpdata main.News -o main/fixtures/news.json
   
   python -Xutf8 manage.py dumpdata geodata.GeoPartWorld -o geodata/fixtures/parts_world.json
   python -Xutf8 manage.py dumpdata geodata.GeoRegionWorld -o geodata/fixtures/regions_world.json
   python -Xutf8 manage.py dumpdata geodata.GeoCountry -o geodata/fixtures/countries.json
   python -Xutf8 manage.py dumpdata geodata.GeoNodeType -o geodata/fixtures/node_types.json
   python -Xutf8 manage.py dumpdata geodata.GeoStreetType -o geodata/fixtures/street_types.json
   
   python -Xutf8 manage.py dumpdata geodata.GeoNode -o geodata/fixtures/frozen_nodes.json
   python -Xutf8 manage.py dumpdata geodata.GeoCity -o geodata/fixtures/frozen_cities.json
   
   python -Xutf8 manage.py dumpdata geodata.GeoStreet -o geodata/fixtures/streets.json
   python -Xutf8 manage.py dumpdata geodata.BaseAddress -o geodata/fixtures/base_addresses.json
   python -Xutf8 manage.py dumpdata geodata.Address -o geodata/fixtures/addresses.json
```

### Загрузка данных

```bash
   python manage.py loaddata shaurma_categories.json
   python manage.py loaddata shaurma.json
   python manage.py loaddata reviews.json
   python manage.py loaddata locations.json
   python manage.py loaddata achievements.json
   python manage.py loaddata stocks.json
   python manage.py loaddata promocodes.json
   python manage.py loaddata shaurma_images.json
   python manage.py loaddata news_tags.json
   python manage.py loaddata news.json
   
   python manage.py loaddata parts_world.json
   python manage.py loaddata regions_world.json
   python manage.py loaddata countries.json
   python manage.py loaddata node_types.json
   python manage.py loaddata street_types.json
   
   python manage.py create_timezones
   
   python manage.py download_geodata
   python manage.py load_states_data
   python manage.py load_cities_data
   
   python manage.py loaddata streets.json
   python manage.py loaddata base_addresses.json
   python manage.py loaddata addresses.json
```


## 🔧 Уникальные команды

1. **Вывод древовидной структуры каталога:**
   ```bash
   python manage.py build_tree <каталог>
   ```

2. **Удаление кэша:**
   ```bash
   python manage.py delete_cache
   ```

3. **Удаление логов:**
   ```bash
   python manage.py delete_logs
   ```


## 📚 Документация

Полная документация проекта доступна в директории `docs/`:

- **[Структура документации](docs/structure.md)** — описание организации документации
- **[Установка и настройка](docs/installation.md)** — подробная инструкция по установке
- **[Архитектура проекта](docs/architecture.md)** — обзор архитектуры и технологий
- **[Документация по приложениям](docs/applications/main/index.md)** — детальная документация каждого приложения
- **[Руководство для разработчиков](docs/development/index.md)** — расширенное руководство по разработке
- **[Справочник](docs/reference/index.md)** — команды и полезные ссылки

### Просмотр документации

Для просмотра документации через MkDocs:

```bash
mkdocs serve
```

Документация будет доступна по адресу: `http://localhost:8000/docs/`


## 📝 Заметки

- Проект использует Jinja2 для шаблонов (расширение `.jinja`)
- Все логи сохраняются в директории `logs/` и разбиты по разделам
- Для разработки доступен Django Debug Toolbar (активируется через `IS_DDT_ACTIVE=True` в `.env`)
- Изображения товаров автоматически оптимизируются через django-imagekit
- Документация организована по приложениям для удобства навигации
