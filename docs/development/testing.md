# Тестирование

## Настройка pytest

Проект использует `pytest` и `pytest-django`. Конфигурация в `pytest.ini`.

### Установка

```bash
pip install pytest pytest-django
```

### Конфигурация

```ini
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = Shaurmania.settings
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
```

## Написание тестов

### Структура тестов

Создавайте тесты в директории `tests/` каждого приложения:

```
main/tests/
├── __init__.py
├── test_models.py
├── test_views.py
├── test_forms.py
└── test_factories.py
```

### Тестирование моделей

```python
# main/tests/test_models.py
import pytest
from django.core.exceptions import ValidationError
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
    assert user.is_staff is False

@pytest.mark.django_db
def test_user_age_validation():
    from datetime import date
    from Shaurmania.settings import MIN_AGE_REGISTRATION
    
    today = date.today()
    invalid_date = today.replace(year=today.year - MIN_AGE_REGISTRATION + 1)
    
    with pytest.raises(ValidationError):
        user = User(
            name='Test',
            email='test@example.com',
            username='testuser',
            date_of_birth=invalid_date
        )
        user.full_clean()
```

### Тестирование представлений

```python
# main/tests/test_views.py
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

@pytest.mark.django_db
def test_product_view(client):
    shaurma = Shaurma.objects.create(
        name='Test Shaurma',
        slug='test-shaurma',
        price=250,
        weight=300,
        compound='Test'
    )
    
    response = client.get(reverse('product', args=[shaurma.slug]))
    assert response.status_code == 200
    assert shaurma.name in response.content.decode()
```

### Тестирование форм

```python
# main/tests/test_forms.py
import pytest
from main.forms import ShaurmaForm

@pytest.mark.django_db
def test_shaurma_form_valid():
    form_data = {
        'name': 'Test Shaurma',
        'price': 250,
        'weight': 300,
        'compound': 'Test'
    }
    form = ShaurmaForm(data=form_data)
    assert form.is_valid()

@pytest.mark.django_db
def test_shaurma_form_invalid():
    form_data = {
        'name': '',  # Пустое имя
        'price': -100  # Отрицательная цена
    }
    form = ShaurmaForm(data=form_data)
    assert not form.is_valid()
```

## Factory Boy

### Создание фабрик

```python
# main/factories/user.py
import factory
from main.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    name = factory.Faker('first_name', locale='ru_RU')
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
```

### Использование в тестах

```python
import pytest
from main.factories import UserFactory, ShaurmaFactory

@pytest.mark.django_db
def test_with_factories():
    user = UserFactory()
    shaurma = ShaurmaFactory()
    
    assert user.username.startswith('user')
    assert shaurma.price > 0
```

### Создание нескольких объектов

```python
@pytest.mark.django_db
def test_multiple_objects():
    users = UserFactory.create_batch(5)
    assert len(users) == 5
```

## Запуск тестов

### Все тесты

```bash
pytest
```

### С подробным выводом

```bash
pytest -v
```

### Конкретный файл

```bash
pytest main/tests/test_models.py
```

### Конкретный тест

```bash
pytest main/tests/test_models.py::test_user_creation
```

### С покрытием кода

```bash
# Через management команду
python manage.py coverage

# Или напрямую
pytest --cov=main --cov-report=html
```

## Фикстуры

### Создание фикстур

```python
# conftest.py
import pytest

@pytest.fixture
def user():
    from main.factories import UserFactory
    return UserFactory()

@pytest.fixture
def shaurma():
    from main.factories import ShaurmaFactory
    return ShaurmaFactory()
```

### Использование фикстур

```python
@pytest.mark.django_db
def test_with_fixtures(user, shaurma):
    assert user.is_active
    assert shaurma.is_available
```

## Моки и стабы

```python
from unittest.mock import patch, MagicMock

@pytest.mark.django_db
@patch('main.services.send_email')
def test_email_sending(mock_send_email):
    # Тест с моком
    mock_send_email.return_value = True
    # ... логика теста
    mock_send_email.assert_called_once()
```

## Параметризация тестов

```python
@pytest.mark.parametrize('price,expected', [
    (100, True),
    (0, False),
    (-10, False),
])
@pytest.mark.django_db
def test_price_validation(price, expected):
    shaurma = ShaurmaFactory.build(price=price)
    assert (shaurma.price > 0) == expected
```

## Лучшие практики

1. **Используйте Factory Boy** для создания тестовых данных
2. **Тестируйте граничные случаи** (пустые значения, отрицательные числа)
3. **Используйте фикстуры** для переиспользования данных
4. **Пишите независимые тесты** (каждый тест должен работать отдельно)
5. **Используйте параметризацию** для тестирования множества значений
6. **Покрывайте тестами** критичную бизнес-логику
7. **Используйте моки** для внешних зависимостей

