# Модели приложения `cart`

## Обзор

Приложение `cart` содержит модели для корзины покупок, заказов и промокодов.

## `Cart`

Корзина покупок пользователя (или сессии).

| Поле         | Тип                       | Параметры                                        | Описание                          |
|--------------|---------------------------|--------------------------------------------------|-----------------------------------|
| `user`       | ForeignKey                | → main.User, on_delete=CASCADE, null=True       | Пользователь (если авторизован)  |
| `session_key`| CharField                 | max_length=40, null=True, blank=True            | Ключ сессии (для анонима)        |
| `item`       | ForeignKey                | → main.Shaurma, on_delete=CASCADE               | Товар                             |
| `quanity`    | PositiveSmallIntegerField | default=1                                       | Количество                        |
| `meta`       | JSONField                 | null=True, blank=True                           | Доп. данные по позиции (опции)   |
| `created_at` | DateTimeField             | auto_now_add=True                               | Когда позиция добавлена          |
| `updated_at` | DateTimeField             | auto_now=True                                   | Когда позиция изменена           |

**Особенности:**

- Единая таблица для авторизованных и анонимных пользователей:
  - либо заполнено `user`,
  - либо заполнено `session_key`.
- Уникальные ограничения:
  - `uniq_cart_user_item` — один товар в корзине на пользователя;
  - `uniq_cart_session_item` — один товар в корзине на сессию.
- Поле `meta` зарезервировано под будущие опции (размер, соусы, добавки).

**Связи:**

- `user` → `main.User` (N:1)
- `item` → `main.Shaurma` (N:1)

---

## `Order`

Архив позиций оплаченных заказов.

> Один логический заказ может состоять из нескольких строк `Order`
> с одинаковым `order_code` (по одной на каждую позицию корзины).

| Поле           | Тип                | Параметры                                        | Описание                          |
|----------------|--------------------|--------------------------------------------------|-----------------------------------|
| `user`         | ForeignKey         | → main.User, on_delete=SET_NULL, null=True      | Пользователь (может быть `NULL`) |
| `session_key`  | CharField          | max_length=40, null=True, blank=True            | Ключ сессии (для гостей)         |
| `shaurma`      | ForeignKey         | → main.Shaurma, on_delete=PROTECT               | Товар                             |
| `quantity`     | PositiveSmallInt   | default=1                                       | Количество в строке              |
| `unit_price`   | PositiveInteger    | default=0                                       | Цена за единицу на момент заказа |
| `line_subtotal`| PositiveInteger    | default=0                                       | Сумма по строке без скидки       |
| `line_discount`| PositiveInteger    | default=0                                       | Скидка по строке                 |
| `line_total`   | PositiveInteger    | default=0                                       | Сумма по строке с учетом скидки  |
| `order_code`   | CharField          | max_length=20, db_index=True                    | Код заказа (общий для набора)    |
| `promocode`    | ForeignKey         | → cart.Promocode, on_delete=SET_NULL, null=True | Применённый промокод             |
| `order_subtotal`| PositiveInteger   | default=0                                       | Сумма заказа без скидки          |
| `order_discount`| PositiveInteger   | default=0                                       | Общая скидка по заказу           |
| `order_total`  | PositiveInteger    | default=0                                       | Итог к оплате                    |
| `payer_name`   | CharField          | max_length=128, default='Galactical Bank Inc.'  | Учебный платёжный счёт           |
| `is_demo_payment`| BooleanField     | default=True                                    | Флаг учебной оплаты              |
| `date`         | DateTimeField      | auto_now_add=True                               | Дата создания строки заказа      |

**Связи:**

- `user` → `main.User` (N:1), может быть `NULL` для гостевых заказов.
- `shaurma` → `main.Shaurma` (N:1), используется `PROTECT`, чтобы не удалять товар из истории.
- `promocode` → `cart.Promocode` (N:1), опционально.

---

## `Promocode`

Промокоды со скидками.

| Поле        | Тип               | Параметры                             | Описание                       |
|-------------|-------------------|---------------------------------------|--------------------------------|
| `code_name` | CharField         | max_length=20, unique=True            | Текстовый код промокода        |
| `code_uuid` | UUIDField         | default=uuid.uuid4, editable=False    | UUID код промокода             |
| `duration`  | SmallIntegerField | default=7                             | Время жизни (дни)              |
| `discount`  | SmallIntegerField | default=5                             | Скидка в процентах             |
| `date_add`  | DateField         | -                                     | Дата создания                  |
| `date_end`  | DateField         | null=True, blank=True, editable=False | Дата окончания (автогенерация) |

**Автоматическая обработка:**

- Автоматический расчет `date_end` при сохранении: `date_add + duration дней`

**Сортировка:** по полю `date_end` (убывание)

---

## Диаграмма связей

```
main.User
  ├── Cart (1:N)
  └── Order (1:N)

main.Shaurma
  ├── Cart (1:N)
  └── Order (1:N)

Promocode (standalone)
```

