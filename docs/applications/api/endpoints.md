# API Эндпоинты

## Базовый URL

```
/api/
```

## Административные эндпоинты

### GET `/api/admin/factories`

Получить список доступных фабрик для генерации тестовых данных.

**Требования:**

- Аутентификация: Да
- Права: Суперпользователь

**Ответ:**

```json
{
  "available_factories": [
    "achievement",
    "location",
    "review",
    "shaurma",
    "shaurma_category",
    "shaurma_image",
    "stock",
    "user",
    "user_achievement"
  ]
}
```

**Пример запроса:**

```bash
curl -X GET \
  http://localhost:8000/api/admin/factories \
  -H "Cookie: sessionid=your-session-id"
```

---

### GET `/api/admin/factories/<name>?count=N`

Генерирует тестовые данные с помощью Factory Boy.

**Требования:**

- Аутентификация: Да
- Права: Суперпользователь

**Параметры:**

- `name` (path) — название фабрики
- `count` (query, optional) — количество объектов (1-50, по умолчанию: 1)

**Доступные фабрики:**

- `shaurma` — товары
- `shaurma_category` — категории товаров
- `shaurma_image` — изображения товаров
- `location` — локации доставки
- `user` — пользователи
- `achievement` — достижения
- `user_achievement` — достижения пользователей
- `review` — отзывы
- `stock` — акции

**Ответ:**

```json
{
  "factory": "shaurma",
  "count": 5,
  "items": [
    {
      "id": 1,
      "name": "Классическая шаурма",
      "slug": "klassicheskaya-shaurma",
      "price": 250,
      "weight": 300,
      "is_available": true
    }
  ]
}
```

**Пример запроса:**

```bash
curl -X GET \
  "http://localhost:8000/api/admin/factories/shaurma?count=5" \
  -H "Cookie: sessionid=your-session-id"
```

**Ограничения:**

- Максимальное количество: 50
- Минимальное количество: 1
- Генерируются только объекты (не сохраняются в БД)

---

## Публичные эндпоинты

### GET `/api/geo_code/<ip>`

Определяет страну по IP-адресу используя MaxMind GeoIP2.

**Требования:**

- Аутентификация: Нет

**Параметры:**

- `ip` (path) — IP-адрес (IPv4)

**Ответ:**

```json
{
  "id": 1,
  "name_ru": "Россия",
  "name_en": "Russia",
  "name_native": "Россия",
  "iso_code": "RU",
  "latitude": 61.52401,
  "longitude": 105.318756
}
```

**Пример запроса:**

```bash
curl -X GET http://localhost:8000/api/geo_code/8.8.8.8
```

**Используемая база данных:**

- MaxMind GeoIP2 (файл: `ext_database/iplocate-country-ipv4.mmdb`)

---

## Ошибки

### 403 Forbidden

```json
{
  "detail": "Forbidden"
}
```

### 404 Not Found

```json
{
  "detail": "Factory not found"
}
```

### 401 Unauthorized

Возвращается при отсутствии аутентификации.

