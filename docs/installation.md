# Установка и настройка

## Требования

### Системные требования

- **Python 3.12+**
- **pip** или **uv** (для ускоренной установки)
- **SQLite3** (встроен в Python)
- **Git** (для клонирования репозитория)

### Опционально

- **UV** — быстрый менеджер пакетов Python
- **Virtualenv** — для изоляции окружения

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/Cet500/Shaurmania
cd Shaurmania
```

### 2. Создание виртуального окружения

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

**Стандартная установка:**

```bash
pip install -r requirements.txt
```

**С использованием UV (быстрее):**

```bash
uv pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example` и установите
там реальные данные.

### 5. Применение миграций

```bash
python manage.py migrate
```

### 6. Загрузка тестовых данных

См. раздел [Управление данными](#управление-данными)

### 7. Создание суперпользователя

```bash
python manage.py createsuperuser
```

## Запуск проекта

### Режим разработки

```bash
python manage.py runserver
```

Приложение будет доступно по адресу: `http://127.0.0.1:8000`

Админ-панель: `http://127.0.0.1:8000/admin-panel/`

### Пробный запуск (Waitress)

```bash
waitress-serve --port=8000 --threads=4 Shaurmania.wsgi:application
```

### Продакшен (рекомендуется)

Для продакшена рекомендуется использовать связку:

- **Gunicorn** — WSGI сервер
- **Nginx** — веб-сервер и reverse proxy

**Пример запуска с Gunicorn:**

```bash
gunicorn Shaurmania.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## Управление данными

### Сохранение данных (dumpdata)

```bash
# Основные данные
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

# Геоданные
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

### Загрузка данных (loaddata)

```bash
# Основные данные
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

# Геоданные
python manage.py loaddata parts_world.json
python manage.py loaddata regions_world.json
python manage.py loaddata countries.json
python manage.py loaddata node_types.json
python manage.py loaddata street_types.json

# Создание часовых поясов
python manage.py create_timezones

# Загрузка геоданных
python manage.py download_geodata
python manage.py load_states_data
python manage.py load_cities_data

# Адреса
python manage.py loaddata streets.json
python manage.py loaddata base_addresses.json
python manage.py loaddata addresses.json
```

## Уникальные команды управления

### Вывод древовидной структуры каталога

```bash
python manage.py build_tree <путь_к_каталогу>
```

### Удаление кэша

```bash
python manage.py delete_cache
```

### Удаление логов

```bash
python manage.py delete_logs
```

### Покрытие кода тестами

```bash
python manage.py coverage
```

## Настройка Django Debug Toolbar

Для активации Django Debug Toolbar установите в `.env`:

```
IS_DDT_ACTIVE=True
```

После этого перезапустите сервер разработки.

## Настройка Telegram бота

1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Получите токен бота
3. Добавьте токен в `.env`:
   ```
   TELEGRAM_BOT_TOKEN=your-bot-token-here
   ```
4. Запустите бота:
   ```bash
   python bot/bot.py
   ```

## Решение проблем

### Проблема с кодировкой при загрузке данных

Используйте флаг `-Xutf8`:

```bash
python -Xutf8 manage.py dumpdata ...
```

### Проблемы с миграциями

Если возникли проблемы с миграциями:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Проблемы с правами доступа к файлам

Убедитесь, что директории `media/`, `static_root/`, `logs/` имеют права на запись.

### Проблемы с изображениями

Убедитесь, что установлены все зависимости для обработки изображений:

```bash
pip install Pillow pilkit
```
