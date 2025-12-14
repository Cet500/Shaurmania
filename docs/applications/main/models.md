# Модели приложения `main`

## Обзор

Приложение `main` содержит модели для пользователей, товаров, отзывов, локаций, достижений, новостей и акций.

## Модели пользователей

### `User`

Кастомная модель пользователя, заменяющая стандартную Django User модель.

| Поле            | Тип              | Параметры                                              | Описание                    |
|-----------------|------------------|--------------------------------------------------------|-----------------------------|
| `name`          | CharField        | max_length=40, validators=[validate_not_in_stop_words] | Имя пользователя            |
| `lastname`      | CharField        | max_length=40, null=True, blank=True                   | Фамилия                     |
| `patronymic`    | CharField        | max_length=40, null=True, blank=True                   | Отчество                    |
| `description`   | CharField        | max_length=240, blank=True                             | Описание профиля            |
| `last_address`  | CharField        | max_length=200, blank=True                             | Адрес последней доставки    |
| `sex`           | CharField        | max_length=1, default='N', choices=SEX                 | Пол (M/F/O/N)               |
| `main_lang`     | CharField        | max_length=2, default='RU', choices=LANGS              | Язык (RU/EN)                |
| `username`      | CharField        | max_length=60, unique=True, db_index=True              | Уникальный логин            |
| `email`         | EmailField       | max_length=80, unique=True, db_index=True              | Email адрес                 |
| `email_status`  | CharField        | max_length=1, default='N', choices=VERIFY_STATUSES     | Статус верификации email    |
| `phone`         | PhoneNumberField | unique=True, null=True, blank=True, db_index=True      | Телефонный номер            |
| `phone_status`  | CharField        | max_length=1, default='N', choices=VERIFY_STATUSES     | Статус верификации телефона |
| `date_of_birth` | DateField        | null=True, blank=True, validators=[validate_age]       | Дата рождения               |
| `register_at`   | DateTimeField    | auto_now_add=True, db_index=True                       | Время регистрации           |
| `updated_at`    | DateTimeField    | auto_now=True                                          | Время обновления            |
| `is_open`       | BooleanField     | default=True, db_index=True                            | Открытый профиль            |
| `is_active`     | BooleanField     | default=True, db_index=True                            | Активный профиль            |
| `is_staff`      | BooleanField     | default=False, db_index=True                           | Сотрудник сайта             |

**Валидация:**

- Проверка на стоп-слова в `name` и `username`
- Валидация возраста (MIN_AGE_REGISTRATION - MAX_AGE_REGISTRATION)
- Валидация email через EmailValidator

**Свойства:**

- `avatar_48_url` — URL аватара 48x48 или дефолтный

**Связи:**

- `avatars` → `UserAvatar` (1:N)
- `addresses` → `UserAddress` (1:N)
- `social_links` → `UserSocialLink` (1:N)
- `user_achievements` → `UserAchievement` (1:N)

---

### `UserAvatar`

Аватары пользователей с автоматическим созданием миниатюр.

| Поле          | Тип            | Параметры                                         | Описание             |
|---------------|----------------|---------------------------------------------------|----------------------|
| `user`        | ForeignKey     | → User, on_delete=CASCADE, related_name='avatars' | Пользователь         |
| `avatar`      | ImageField     | upload_to='user_avatars', null=True, blank=True   | Исходное изображение |
| `is_primary`  | BooleanField   | default=False                                     | Основной аватар      |
| `avatar_32x`  | ImageSpecField | source='avatar', 32x32, PNG, quality=100          | Миниатюра 32x32      |
| `avatar_48x`  | ImageSpecField | source='avatar', 48x48, PNG, quality=100          | Миниатюра 48x48      |
| `avatar_64x`  | ImageSpecField | source='avatar', 64x64, PNG, quality=100          | Миниатюра 64x64      |
| `avatar_96x`  | ImageSpecField | source='avatar', 96x96, PNG, quality=100          | Миниатюра 96x96      |
| `avatar_128x` | ImageSpecField | source='avatar', 128x128, PNG, quality=100        | Миниатюра 128x128    |
| `avatar_192x` | ImageSpecField | source='avatar', 192x192, PNG, quality=100        | Миниатюра 192x192    |

**Обработка изображений:**

- Автоматическое создание миниатюр через ImageKit
- Формат: PNG, качество: 100%

---

### `UserAddress`

Адреса пользователей, связанные с геоданными.

| Поле         | Тип          | Параметры                                           | Описание           |
|--------------|--------------|-----------------------------------------------------|--------------------|
| `user`       | ForeignKey   | → User, on_delete=CASCADE, related_name='addresses' | Пользователь       |
| `address`    | ForeignKey   | → geodata.Address, on_delete=PROTECT                | Адрес из геоданных |
| `is_default` | BooleanField | default=False                                       | Адрес по умолчанию |

---

### `UserSocialLink`

Социальные ссылки пользователей.

| Поле       | Тип        | Параметры                                              | Описание                       |
|------------|------------|--------------------------------------------------------|--------------------------------|
| `user`     | ForeignKey | → User, on_delete=CASCADE, related_name='social_links' | Пользователь                   |
| `platform` | CharField  | max_length=50                                          | Платформа (VK, Telegram, etc.) |
| `url`      | URLField   | max_length=200, validators=[validate_social_link]      | Ссылка                         |

---

## Модели товаров

### `Shaurma`

Основная модель товара — шаурма.

| Поле            | Тип                       | Параметры                                                    | Описание                  |
|-----------------|---------------------------|--------------------------------------------------------------|---------------------------|
| `name`          | CharField                 | max_length=60, unique=True                                   | Название                  |
| `slug`          | SlugField                 | max_length=70, blank=True                                    | URL-адрес (автогенерация) |
| `category`      | ForeignKey                | → ShaurmaCategory, on_delete=SET_NULL, null=True, blank=True | Категория                 |
| `compound`      | TextField                 | max_length=600                                               | Состав                    |
| `short_text`    | TextField                 | max_length=200, blank=True                                   | Краткое описание          |
| `description`   | TextField                 | max_length=1000, blank=True                                  | Описание                  |
| `history`       | TextField                 | max_length=1000, blank=True                                  | История блюда             |
| `picture`       | ImageField                | upload_to='shaurma_images'                                   | Основное изображение      |
| `thumbnail_md`  | ImageSpecField            | source='picture', 640x450, PNG, quality=90                   | Средняя миниатюра         |
| `thumbnail_sm`  | ImageSpecField            | source='picture', 285x200, PNG, quality=90                   | Маленькая миниатюра       |
| `price`         | PositiveSmallIntegerField | -                                                            | Цена в рублях             |
| `weight`        | PositiveSmallIntegerField | -                                                            | Вес в граммах             |
| `calories`      | PositiveIntegerField      | default=0                                                    | Калории (ккал)            |
| `proteins`      | FloatField                | default=0                                                    | Белки (г)                 |
| `fats`          | FloatField                | default=0                                                    | Жиры (г)                  |
| `carbohydrates` | FloatField                | default=0                                                    | Углеводы (г)              |
| `is_available`  | BooleanField              | default=True                                                 | Доступна для заказа       |
| `created_at`    | DateTimeField             | auto_now_add=True                                            | Дата создания             |
| `updated_at`    | DateTimeField             | auto_now=True                                                | Дата обновления           |

**Автоматическая обработка:**

- Генерация `slug` из названия при сохранении
- Автоматическое создание миниатюр при загрузке изображения

**Связи:**

- `images` → `ShaurmaImage` (1:N)
- `reviews` → `Review` (1:N)
- `cart_items` → `cart.Cart` (1:N)
- `orders` → `cart.Order` (1:N)

---

### `ShaurmaCategory`

Категории шаурмы.

| Поле          | Тип                       | Параметры         | Описание           |
|---------------|---------------------------|-------------------|--------------------|
| `name`        | CharField                 | max_length=60     | Название           |
| `description` | TextField                 | max_length=200    | Описание           |
| `order`       | PositiveSmallIntegerField | default=0         | Порядок сортировки |
| `created_at`  | DateTimeField             | auto_now_add=True | Дата создания      |
| `updated_at`  | DateTimeField             | auto_now=True     | Дата обновления    |

**Сортировка:** по полю `order`, затем по `name`

**Связи:**

- `shaurmas` → `Shaurma` (1:N)

---

### `ShaurmaImage`

Дополнительные изображения товаров.

| Поле           | Тип                  | Параметры                                               | Описание            |
|----------------|----------------------|---------------------------------------------------------|---------------------|
| `shaurma`      | ForeignKey           | → Shaurma, on_delete=CASCADE, related_name='images'     | Товар               |
| `image`        | ImageField           | upload_to='shaurma_additional'                          | Изображение         |
| `thumbnail_md` | ImageSpecField       | source='image', 550x310, PNG, quality=90                | Миниатюра           |
| `caption`      | CharField            | max_length=100, default='Фото нашей шаурмы', blank=True | Подпись             |
| `order`        | PositiveIntegerField | default=0                                               | Порядок отображения |
| `created_at`   | DateTimeField        | auto_now_add=True                                       | Дата добавления     |
| `updated_at`   | DateTimeField        | auto_now=True                                           | Дата обновления     |

---

## Модели отзывов

### `Review`

Отзывы о товарах.

| Поле         | Тип                       | Параметры                                           | Описание            |
|--------------|---------------------------|-----------------------------------------------------|---------------------|
| `name`       | CharField                 | max_length=60                                       | Имя автора          |
| `text`       | TextField                 | max_length=600                                      | Текст отзыва        |
| `rating`     | PositiveSmallIntegerField | choices=[1,2,3,4,5]                                 | Рейтинг (звезды)    |
| `shaurma`    | ForeignKey                | → Shaurma, on_delete=CASCADE, null=True, blank=True | Товар (опционально) |
| `created_at` | DateTimeField             | auto_now_add=True                                   | Дата создания       |

---

## Модели локаций

### `Location`

Точки доставки (заведения).

| Поле          | Тип           | Параметры                                          | Описание                  |
|---------------|---------------|----------------------------------------------------|---------------------------|
| `name`        | CharField     | max_length=60                                      | Название                  |
| `slug`        | SlugField     | max_length=70, blank=True                          | URL-адрес (автогенерация) |
| `description` | TextField     | max_length=600                                     | Описание                  |
| `planet`      | CharField     | max_length=60, default='Земля'                     | Планета                   |
| `country`     | CharField     | max_length=60, default='Россия'                    | Страна                    |
| `city`        | CharField     | max_length=30                                      | Город                     |
| `address`     | CharField     | max_length=60                                      | Адрес                     |
| `picture`     | ImageField    | upload_to='locations'                              | Изображение локации       |
| `timeline`    | CharField     | max_length=3, default='NOW', choices=TIME_VARIANTS | Временной период          |
| `contacts`    | CharField     | max_length=60                                      | Контакты                  |
| `open_hours`  | TimeField     | -                                                  | Время открытия            |
| `close_hours` | TimeField     | -                                                  | Время закрытия            |
| `created_at`  | DateTimeField | auto_now_add=True                                  | Дата добавления           |
| `updated_at`  | DateTimeField | auto_now=True                                      | Дата обновления           |

**Автоматическая обработка:**

- Генерация `slug` из названия при сохранении

---

## Модели достижений

### `Achievement`

Достижения системы.

| Поле      | Тип        | Параметры                     | Описание               |
|-----------|------------|-------------------------------|------------------------|
| `name`    | CharField  | max_length=60                 | Название               |
| `picture` | ImageField | upload_to='achievement_image' | Изображение достижения |

**Связи:**

- `user_achievements` → `UserAchievement` (1:N)

---

### `UserAchievement`

Достижения пользователей.

| Поле          | Тип           | Параметры                        | Описание       |
|---------------|---------------|----------------------------------|----------------|
| `user`        | ForeignKey    | → User, on_delete=CASCADE        | Пользователь   |
| `achievement` | ForeignKey    | → Achievement, on_delete=CASCADE | Достижение     |
| `get_date`    | DateTimeField | auto_now_add=True                | Дата получения |

---

## Модели новостей

### `News`

Новости сайта.

| Поле           | Тип             | Параметры                                      | Описание                  |
|----------------|-----------------|------------------------------------------------|---------------------------|
| `title`        | CharField       | max_length=200                                 | Заголовок                 |
| `slug`         | SlugField       | max_length=220, blank=True                     | URL-адрес (автогенерация) |
| `text`         | TextField       | -                                              | Текст новости             |
| `image`        | ImageField      | upload_to='news_images', null=True, blank=True | Изображение               |
| `tags`         | ManyToManyField | → NewsTag, blank=True                          | Теги                      |
| `published_at` | DateTimeField   | null=True, blank=True                          | Дата публикации           |
| `created_at`   | DateTimeField   | auto_now_add=True                              | Дата создания             |
| `updated_at`   | DateTimeField   | auto_now=True                                  | Дата обновления           |

**Связи:**

- `tags` → `NewsTag` (M:N)

---

### `NewsTag`

Теги новостей.

| Поле   | Тип       | Параметры                  | Описание                  |
|--------|-----------|----------------------------|---------------------------|
| `name` | CharField | max_length=50, unique=True | Название                  |
| `slug` | SlugField | max_length=60, blank=True  | URL-адрес (автогенерация) |

**Связи:**

- `news` → `News` (M:N)

---

## Модели акций

### `Stock`

Акции и скидки.

| Поле               | Тип                       | Параметры                 | Описание                  |
|--------------------|---------------------------|---------------------------|---------------------------|
| `name`             | CharField                 | max_length=60             | Название                  |
| `slug`             | SlugField                 | max_length=70, blank=True | URL-адрес (автогенерация) |
| `description`      | TextField                 | -                         | Описание                  |
| `image`            | ImageField                | upload_to='stocks'        | Изображение акции         |
| `discount_percent` | PositiveSmallIntegerField | -                         | Процент скидки            |
| `start_date`       | DateField                 | -                         | Дата начала               |
| `end_date`         | DateField                 | -                         | Дата окончания            |
| `is_active`        | BooleanField              | default=True              | Активна                   |
| `created_at`       | DateTimeField             | auto_now_add=True         | Дата создания             |
| `updated_at`       | DateTimeField             | auto_now=True             | Дата обновления           |

---

## Модели доставки

### `Delivery`

Информация о доставке.

| Поле            | Тип                       | Параметры         | Описание           |
|-----------------|---------------------------|-------------------|--------------------|
| `city`          | CharField                 | max_length=60     | Город              |
| `address`       | CharField                 | max_length=200    | Адрес              |
| `delivery_time` | CharField                 | max_length=50     | Время доставки     |
| `delivery_cost` | PositiveSmallIntegerField | -                 | Стоимость доставки |
| `created_at`    | DateTimeField             | auto_now_add=True | Дата создания      |

---

## Диаграмма связей

```
User
  ├── UserAvatar (1:N)
  ├── UserAddress (1:N)
  ├── UserSocialLink (1:N)
  └── UserAchievement (1:N)
      └── Achievement (N:1)

ShaurmaCategory
  └── Shaurma (1:N)
      ├── ShaurmaImage (1:N)
      ├── Review (1:N)
      ├── Cart (1:N) [cart app]
      └── Order (1:N) [cart app]

NewsTag
  └── News (M:N)

Location (standalone)
Stock (standalone)
Delivery (standalone)
```

