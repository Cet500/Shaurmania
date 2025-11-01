# ШаурМания

Сайт по продаже шаурмы с доставкой на Django.


## 📋 Описание

ШаурМания — это веб-приложение для заказа шаурмы с доставкой.
Проект включает систему управления товарами, корзину покупок, 
промокоды, достижения, локации доставки и систему отзывов.

> **Версия данных:** 6


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
| **Backend**               | Django 6.0 (beta)           |
| **База данных**           | SQLite3                     |
| **Шаблоны**               | Jinja2 (через django-jinja) |
| **Обработка изображений** | django-imagekit             |
| **Сжатие статики**        | django-compressor           |
| **Тестирование**          | pytest, pytest-django       |
| **Боты**                  | aiogram 3.x (Telegram)      |


## 📦 Требования

- Python 3.12+
- venv
- pip
- SQLite
- UV ( по желанию, для скорости )


## 🚀 Установка и настройка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Cet500/Shaurmania
   cd Shaurmania
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
   или
   ```bash
   uv pip install -r requirements.txt
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

2. **Пробный запуск:**
   ```bash
   waitress-serve --port=8000 --threads=4 Shaurmania.wsgi:application
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
├── bot/               # Telegram бот
├── cart/              # Приложение корзины (корзина, заказы, промокоды)
├── logs/              # Логи приложения
├── main/              # Основное приложение (товары, пользователи, отзывы, локации)
├── media/             # Загружаемые файлы (изображения товаров, аватары)
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


## 📝 Заметки

- Проект использует Jinja2 для шаблонов (расширение `.jinja`)
- Все логи сохраняются в директории `logs/` и разбиты по разделам.
- Для разработки доступен Django Debug Toolbar (активируется через `IS_DDT_ACTIVE=True` в `.env`)
- Изображения товаров автоматически оптимизируются через django-imagekit
