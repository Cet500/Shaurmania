# Модели приложения `geodata`

## Обзор

Приложение `geodata` содержит модели для географической иерархии, адресов и часовых поясов.

## Географическая иерархия

### `GeoPartWorld`

Части света.

| Поле      | Тип       | Параметры      | Описание               |
|-----------|-----------|----------------|------------------------|
| `name_ru` | CharField | max_length=250 | Название на русском    |
| `name_en` | CharField | max_length=250 | Название на английском |

---

### `GeoRegionWorld`

Регионы мира.

| Поле      | Тип       | Параметры      | Описание               |
|-----------|-----------|----------------|------------------------|
| `name_ru` | CharField | max_length=250 | Название на русском    |
| `name_en` | CharField | max_length=250 | Название на английском |

---

### `GeoCountry`

Страны.

| Поле          | Тип        | Параметры                                         | Описание               |
|---------------|------------|---------------------------------------------------|------------------------|
| `name_ru`     | CharField  | max_length=250, db_index=True                     | Название на русском    |
| `name_en`     | CharField  | max_length=250                                    | Название на английском |
| `name_native` | CharField  | max_length=250                                    | Родное название        |
| `iso_code`    | CharField  | max_length=10, unique=True                        | ISO код страны         |
| `latitude`    | FloatField | null=True, blank=True, validators=[-90.0, 90.0]   | Широта центра          |
| `longitude`   | FloatField | null=True, blank=True, validators=[-180.0, 180.0] | Долгота центра         |

**Связи:**

- `nodes` → `GeoNode` (1:N)

---

### `GeoNodeType`

Типы географических узлов (область, край, республика и т.д.).

| Поле      | Тип       | Параметры      | Описание               |
|-----------|-----------|----------------|------------------------|
| `name_ru` | CharField | max_length=100 | Название на русском    |
| `name_en` | CharField | max_length=100 | Название на английском |

**Связи:**

- `nodes` → `GeoNode` (1:N)

---

### `GeoNode`

Географические узлы (федеральные округа, регионы, области).

| Поле           | Тип                       | Параметры                                                                 | Описание               |
|----------------|---------------------------|---------------------------------------------------------------------------|------------------------|
| `country`      | ForeignKey                | → GeoCountry, on_delete=CASCADE, related_name='nodes'                     | Страна                 |
| `node_type`    | ForeignKey                | → GeoNodeType, on_delete=CASCADE, related_name='nodes'                    | Тип узла               |
| `parent`       | ForeignKey                | → self, on_delete=CASCADE, null=True, blank=True, related_name='children' | Родительский узел      |
| `level`        | PositiveSmallIntegerField | null=True, blank=True                                                     | Уровень в иерархии     |
| `name_ru`      | CharField                 | max_length=250, db_index=True                                             | Название на русском    |
| `name_en`      | CharField                 | max_length=250                                                            | Название на английском |
| `name_native`  | CharField                 | max_length=250                                                            | Родное название        |
| `latitude`     | FloatField                | null=True, blank=True, validators=[-90.0, 90.0]                           | Широта центра          |
| `longitude`    | FloatField                | null=True, blank=True, validators=[-180.0, 180.0]                         | Долгота центра         |
| `timezone`     | ForeignKey                | → TimeZone, on_delete=CASCADE                                             | Часовой пояс           |
| `population`   | BigIntegerField           | null=True, blank=True                                                     | Население              |
| `iso_code`     | CharField                 | max_length=20, blank=True, null=True                                      | ISO 3166-2 код         |
| `wiki_data_id` | CharField                 | max_length=30, blank=True, null=True                                      | ID в Wikidata          |
| `created_at`   | DateTimeField             | db_index=True                                                             | Дата создания          |
| `updated_at`   | DateTimeField             | db_index=True                                                             | Дата обновления        |

**Свойства:**

- `full_path` — полный путь от страны до узла
- `name_with_type` — название с типом
- `wiki_data_url` — URL в Wikidata

**Связи:**

- `children` → `GeoNode` (1:N, self-reference)
- `cities` → `GeoCity` (1:N)

---

### `GeoCity`

Города.

| Поле          | Тип             | Параметры                                         | Описание               |
|---------------|-----------------|---------------------------------------------------|------------------------|
| `country`     | ForeignKey      | → GeoCountry, on_delete=CASCADE                   | Страна                 |
| `node`        | ForeignKey      | → GeoNode, on_delete=CASCADE                      | Регион                 |
| `name_ru`     | CharField       | max_length=250, db_index=True                     | Название на русском    |
| `name_en`     | CharField       | max_length=250                                    | Название на английском |
| `name_native` | CharField       | max_length=250                                    | Родное название        |
| `latitude`    | FloatField      | null=True, blank=True, validators=[-90.0, 90.0]   | Широта                 |
| `longitude`   | FloatField      | null=True, blank=True, validators=[-180.0, 180.0] | Долгота                |
| `population`  | BigIntegerField | null=True, blank=True                             | Население              |

**Связи:**

- `streets` → `GeoStreet` (1:N)

---

### `GeoStreetType`

Типы улиц (улица, проспект, переулок и т.д.).

| Поле      | Тип       | Параметры      | Описание               |
|-----------|-----------|----------------|------------------------|
| `name_ru` | CharField | max_length=100 | Название на русском    |
| `name_en` | CharField | max_length=100 | Название на английском |

**Связи:**

- `streets` → `GeoStreet` (1:N)

---

### `GeoStreet`

Улицы.

| Поле          | Тип        | Параметры                                                  | Описание               |
|---------------|------------|------------------------------------------------------------|------------------------|
| `city`        | ForeignKey | → GeoCity, on_delete=CASCADE, related_name='streets'       | Город                  |
| `street_type` | ForeignKey | → GeoStreetType, on_delete=CASCADE, related_name='streets' | Тип улицы              |
| `name_ru`     | CharField  | max_length=250, db_index=True                              | Название на русском    |
| `name_en`     | CharField  | max_length=250                                             | Название на английском |
| `name_native` | CharField  | max_length=250                                             | Родное название        |

**Связи:**

- `base_addresses` → `BaseAddress` (1:N)

---

## Адреса

### `BaseAddress`

Базовый адрес с денормализацией данных.

| Поле             | Тип           | Параметры                                             | Описание                              |
|------------------|---------------|-------------------------------------------------------|---------------------------------------|
| `street`         | ForeignKey    | → GeoStreet, on_delete=PROTECT                        | Улица                                 |
| `city`           | ForeignKey    | → GeoCity, on_delete=PROTECT, editable=False          | Город (денормализовано)               |
| `node`           | ForeignKey    | → GeoNode, on_delete=PROTECT, editable=False          | Регион (денормализовано)              |
| `country`        | ForeignKey    | → GeoCountry, on_delete=PROTECT, editable=False       | Страна (денормализовано)              |
| `house`          | CharField     | max_length=30, db_index=True                          | Дом/здание                            |
| `building`       | CharField     | max_length=10, blank=True                             | Корпус/строение                       |
| `postal_code`    | CharField     | max_length=10, blank=True, null=True                  | Почтовый индекс                       |
| `full_address`   | CharField     | max_length=500, blank=True, null=True, editable=False | Полный адрес (автогенерация)          |
| `normal_address` | CharField     | max_length=500, blank=True, null=True, editable=False | Нормализованный адрес (автогенерация) |
| `latitude`       | FloatField    | null=True, blank=True, validators=[-90.0, 90.0]       | Широта                                |
| `longitude`      | FloatField    | null=True, blank=True, validators=[-180.0, 180.0]     | Долгота                               |
| `is_verified`    | BooleanField  | default=False                                         | Подтвержден                           |
| `created_at`     | DateTimeField | auto_now_add=True                                     | Дата создания                         |
| `updated_at`     | DateTimeField | auto_now=True                                         | Дата обновления                       |

**Особенности:**

- Денормализация данных для оптимизации запросов
- Автоматическая генерация полного адреса
- Геокодирование через внешний API

**Связи:**

- `addresses` → `Address` (1:N)

---

### `Address`

Расширенная версия BaseAddress (наследуется или расширяет функциональность).

| Поле                    | Тип           | Параметры                        | Описание                |
|-------------------------|---------------|----------------------------------|-------------------------|
| `base_address`          | OneToOneField | → BaseAddress, on_delete=CASCADE | Базовый адрес           |
| *(дополнительные поля)* | -             | -                                | Расширенные поля адреса |

**Связи:**

- `user_addresses` → `main.UserAddress` (1:N)

---

## Часовые пояса

### `TimeZone`

Часовые пояса.

| Поле     | Тип               | Параметры                   | Описание                             |
|----------|-------------------|-----------------------------|--------------------------------------|
| `name`   | CharField         | max_length=100, unique=True | Название (например, "Europe/Moscow") |
| `offset` | SmallIntegerField | -                           | Смещение от UTC в часах              |

**Связи:**

- `nodes` → `GeoNode` (1:N)

---

## Диаграмма связей

```
GeoPartWorld
GeoRegionWorld

GeoCountry
  └── GeoNode (1:N)
      ├── GeoNode (1:N, self-reference)
      └── GeoCity (1:N)
          └── GeoStreet (1:N)
              └── BaseAddress (1:N)
                  └── Address (1:1)
                      └── main.UserAddress (1:N)

GeoNodeType
  └── GeoNode (1:N)

GeoStreetType
  └── GeoStreet (1:N)

TimeZone
  └── GeoNode (1:N)
```

