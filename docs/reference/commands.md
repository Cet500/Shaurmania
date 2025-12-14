# Команды

## Управление проектом

### Запуск сервера

```bash
# Сервер разработки (по умолчанию на порту 8000)
python manage.py runserver

# На конкретном порту
python manage.py runserver 8080

# На конкретном IP и порту
python manage.py runserver 0.0.0.0:8000
```

### Миграции

```bash
# Создание миграций для всех приложений
python manage.py makemigrations

# Создание миграций для конкретного приложения
python manage.py makemigrations main

# Применение всех миграций
python manage.py migrate

# Применение миграций для конкретного приложения
python manage.py migrate main

# Откат миграции
python manage.py migrate main 0001

# Просмотр статуса миграций
python manage.py showmigrations

# Просмотр SQL миграции (без применения)
python manage.py sqlmigrate main 0001
```

### Пользователи

```bash
# Создание суперпользователя
python manage.py createsuperuser

# Изменение пароля пользователя
python manage.py changepassword username

# Создание пользователя (через shell)
python manage.py shell
>>> from main.models import User
>>> User.objects.create_user(name='Test', email='test@example.com', username='test', password='pass')
```

### Статические файлы

```bash
# Сбор статических файлов
python manage.py collectstatic

# Сбор без подтверждения
python manage.py collectstatic --noinput

# Очистка старых файлов перед сбором
python manage.py collectstatic --clear
```

## Тестирование

### Django тесты

```bash
# Запуск всех тестов
python manage.py test

# Запуск тестов конкретного приложения
python manage.py test main

# Запуск тестов конкретного файла
python manage.py test main.tests.test_models

# Запуск конкретного теста
python manage.py test main.tests.test_models.TestUser.test_user_creation

# Запуск с подробным выводом
python manage.py test --verbosity=2

# Запуск с сохранением базы данных
python manage.py test --keepdb
```

### pytest

```bash
# Запуск всех тестов
pytest

# С подробным выводом
pytest -v

# С очень подробным выводом
pytest -vv

# Запуск конкретного файла
pytest main/tests/test_models.py

# Запуск конкретного теста
pytest main/tests/test_models.py::test_user_creation

# Запуск с покрытием кода
pytest --cov=main --cov-report=html

# Запуск только быстрых тестов
pytest -m "not slow"

# Запуск с остановкой на первой ошибке
pytest -x
```

### Покрытие кода

```bash
# Через management команду
python manage.py coverage

# Через pytest
pytest --cov=main --cov-report=html --cov-report=term
```

## Управление данными

### Сохранение данных (dumpdata)

```bash
# Сохранение конкретной модели
python -Xutf8 manage.py dumpdata main.Shaurma -o main/fixtures/shaurma.json

# Сохранение всех моделей приложения
python -Xutf8 manage.py dumpdata main -o main/fixtures/all_main.json

# Сохранение с исключением полей
python -Xutf8 manage.py dumpdata main.Shaurma --exclude=main.ShaurmaImage -o shaurma.json

# Сохранение в формате JSON (по умолчанию)
python -Xutf8 manage.py dumpdata main.Shaurma -o shaurma.json

# Сохранение в формате XML
python -Xutf8 manage.py dumpdata main.Shaurma -o shaurma.xml --format=xml

# Сохранение с индентацией
python -Xutf8 manage.py dumpdata main.Shaurma --indent=2 -o shaurma.json
```

### Загрузка данных (loaddata)

```bash
# Загрузка из файла
python manage.py loaddata shaurma.json

# Загрузка из нескольких файлов
python manage.py loaddata shaurma.json reviews.json

# Загрузка из директории fixtures
python manage.py loaddata shaurma_categories.json

# Загрузка с игнорированием ошибок
python manage.py loaddata shaurma.json --verbosity=0
```

### Геоданные

```bash
# Создание часовых поясов
python manage.py create_timezones

# Загрузка геоданных
python manage.py download_geodata

# Загрузка данных о регионах
python manage.py load_states_data

# Загрузка данных о городах
python manage.py load_cities_data
```

## Утилиты

### Структура каталога

```bash
# Вывод древовидной структуры каталога
python manage.py build_tree <путь>

# Пример
python manage.py build_tree static/main
```

### Кэш

```bash
# Удаление кэша
python manage.py delete_cache
```

### Логи

```bash
# Удаление логов
python manage.py delete_logs
```

## Django Shell

### Базовое использование

```bash
# Запуск shell
python manage.py shell

# Запуск shell с IPython (если установлен)
python manage.py shell -i ipython

# Запуск shell с bpython (если установлен)
python manage.py shell -i bpython
```

### Примеры использования shell

```python
# В shell
from main.models import User, Shaurma

# Получить всех пользователей
users = User.objects.all()

# Создать пользователя
user = User.objects.create_user(
    name='Test',
    email='test@example.com',
    username='testuser',
    password='testpass123'
)

# Получить товары
shaurmas = Shaurma.objects.filter(is_available=True)

# Создать товар
shaurma = Shaurma.objects.create(
    name='Классическая шаурма',
    price=250,
    weight=300,
    compound='Лаваш, мясо, овощи'
)
```

## Проверка проекта

### Проверка настроек

```bash
# Проверка конфигурации
python manage.py check

# Проверка конкретного приложения
python manage.py check main

# Проверка с тегами
python manage.py check --tag=security
```

### Информация о проекте

```bash
# Версия Django
python manage.py version

# Список доступных команд
python manage.py help

# Помощь по конкретной команде
python manage.py help migrate
```

## Уникальные команды проекта

### build_tree

Выводит древовидную структуру каталога.

```bash
python manage.py build_tree <каталог>
```

### delete_cache

Удаляет весь кэш проекта.

```bash
python manage.py delete_cache
```

### delete_logs

Удаляет все логи проекта.

```bash
python manage.py delete_logs
```

### coverage

Генерирует отчет о покрытии кода тестами.

```bash
python manage.py coverage
```

## Полезные комбинации

```bash
# Полная перезагрузка проекта
python manage.py migrate
python manage.py collectstatic
python manage.py delete_cache

# Подготовка к тестированию
python manage.py migrate --run-syncdb
python manage.py test

# Очистка перед деплоем
python manage.py collectstatic --clear --noinput
python manage.py migrate
```
