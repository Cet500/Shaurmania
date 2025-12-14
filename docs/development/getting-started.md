# Начало работы

## Настройка окружения разработки

### 1. Клонирование и установка

Следуйте инструкциям из [Установка и настройка](../installation.md):

```bash
git clone https://github.com/Cet500/Shaurmania
cd Shaurmania
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Настройка .env

Создайте файл `.env` на основе `.env.example`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
IS_DDT_ACTIVE=True  # Для разработки
DATABASE_NAME=db.sqlite3
```

### 3. Применение миграций

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Загрузка тестовых данных

```bash
python manage.py loaddata shaurma_categories.json
python manage.py loaddata shaurma.json
# ... и т.д.
```

## Структура проекта

```
Shaurmania/
├── api/                  # API приложение
│   ├── views.py
│   └── urls.py
├── bot/                  # Telegram бот
│   ├── bot.py
│   └── settings.py
├── cart/                 # Корзина и заказы
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── geodata/              # Геоданные
│   ├── models/
│   ├── services/
│   └── management/
├── main/                 # Основное приложение
│   ├── admin/            # Настройки админ-панели
│   ├── factories/        # Factory Boy фабрики
│   ├── fixtures/         # Тестовые данные
│   ├── management/       # Management команды
│   ├── models/           # Модели данных
│   ├── tests/            # Тесты
│   ├── views/            # Представления
│   └── ...
├── security/             # Безопасность
│   ├── models/
│   └── signals.py
├── Shaurmania/           # Настройки проекта
│   ├── settings.py
│   └── urls.py
├── static/               # Статические файлы
├── template/             # Jinja2 шаблоны
├── docs/                 # Документация
└── ...
```

## Рабочий процесс

### Создание новой фичи

1. **Создайте ветку:**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Внесите изменения:**
	- Создайте/измените модели
	- Создайте миграции: `python manage.py makemigrations`
	- Примените миграции: `python manage.py migrate`
	- Создайте представления и URL-маршруты
	- Напишите тесты

3. **Протестируйте:**
   ```bash
   pytest
   python manage.py test
   ```

4. **Создайте Pull Request**

### Работа с моделями

1. Создайте модель в соответствующем приложении
2. Создайте миграцию: `python manage.py makemigrations`
3. Примените миграцию: `python manage.py migrate`
4. Зарегистрируйте в админке
5. Создайте фабрику для тестов (если нужно)

### Работа с представлениями

1. Создайте view в соответствующем модуле `views/`
2. Добавьте URL-маршрут в `urls.py`
3. Создайте шаблон в `template/`
4. Напишите тесты

## Инструменты разработки

### Django Debug Toolbar

Активируйте в `.env`:

```
IS_DDT_ACTIVE=True
```

Показывает:

- SQL запросы
- Время выполнения
- Переменные шаблона
- Статические файлы

### Логирование

Логи разделены по категориям:

- `logs/logs.log` — основные логи
- `logs/django/` — логи Django
- `logs/security/` — логи безопасности
- `logs/errors.log` — только ошибки

Использование:

```python
import logging


logger = logging.getLogger( 'main' )
logger.info( 'Сообщение' )
```

## Следующие шаги

- Изучите [Стиль кода](code-style.md)
- Прочитайте [Работа с моделями](models.md)
- Ознакомьтесь с [Тестированием](testing.md)

