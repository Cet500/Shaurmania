# Модели приложения `cart`

## Обзор

Приложение `cart` содержит модели для корзины покупок, заказов и промокодов.

## `Cart`

Корзина покупок пользователя.

| Поле      | Тип                       | Параметры                         | Описание     |
|-----------|---------------------------|-----------------------------------|--------------|
| `user`    | ForeignKey                | → main.User, on_delete=CASCADE    | Пользователь |
| `item`    | ForeignKey                | → main.Shaurma, on_delete=CASCADE | Товар        |
| `quanity` | PositiveSmallIntegerField | default=1                         | Количество   |

**Особенности:**

- Для авторизованных пользователей — хранение в БД
- Для анонимных пользователей — хранение в сессии Django

**Связи:**

- `user` → `main.User` (N:1)
- `item` → `main.Shaurma` (N:1)

---

## `Order`

Заказы пользователей.

| Поле      | Тип           | Параметры                         | Описание     |
|-----------|---------------|-----------------------------------|--------------|
| `user`    | ForeignKey    | → main.User, on_delete=CASCADE    | Пользователь |
| `shaurma` | ForeignKey    | → main.Shaurma, on_delete=CASCADE | Товар        |
| `date`    | DateTimeField | auto_now_add=True                 | Дата заказа  |

**Связи:**

- `user` → `main.User` (N:1)
- `shaurma` → `main.Shaurma` (N:1)

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

