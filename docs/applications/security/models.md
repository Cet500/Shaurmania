# Модели приложения `security`

## Обзор

Приложение `security` содержит модели для безопасности, мониторинга и логирования.

## `SecurityDevice`

Устройства пользователей с парсингом User-Agent.

| Поле              | Тип           | Параметры                                                                   | Описание                            |
|-------------------|---------------|-----------------------------------------------------------------------------|-------------------------------------|
| `uuid`            | UUIDField     | primary_key=True, default=uuid4, unique=True, db_index=True, editable=False | Уникальный идентификатор устройства |
| `user_agent_full` | CharField     | max_length=255, null=True                                                   | Полный User-Agent                   |
| `browser_name`    | CharField     | max_length=40, null=True                                                    | Название браузера                   |
| `browser_version` | CharField     | max_length=40, null=True                                                    | Полная версия браузера              |
| `browser_major`   | CharField     | max_length=10, null=True                                                    | Основная версия браузера            |
| `device_vendor`   | CharField     | max_length=40, null=True                                                    | Производитель устройства            |
| `device_model`    | CharField     | max_length=40, null=True                                                    | Модель устройства                   |
| `device_type`     | CharField     | max_length=20, null=True                                                    | Тип устройства                      |
| `engine_name`     | CharField     | max_length=20, null=True                                                    | Название движка                     |
| `engine_version`  | CharField     | max_length=20, null=True                                                    | Версия движка                       |
| `os_name`         | CharField     | max_length=40, null=True                                                    | Название ОС                         |
| `os_version`      | CharField     | max_length=20, null=True                                                    | Версия ОС                           |
| `cpu`             | CharField     | max_length=20, null=True                                                    | Процессор                           |
| `created_at`      | DateTimeField | auto_now_add=True                                                           | Время создания                      |

**Методы:**

- `from_user_agent(user_agent_str)` (staticmethod) — создание устройства из User-Agent

**Связи:**

- `auth_logs` → `SecurityAuthLog` (1:N)

---

## `SecurityAuthLog`

Логи авторизаций пользователей.

| Поле            | Тип                   | Параметры                                           | Описание                    |
|-----------------|-----------------------|-----------------------------------------------------|-----------------------------|
| `user`          | ForeignKey            | → main.User, on_delete=CASCADE                      | Пользователь                |
| `device`        | ForeignKey            | → SecurityDevice, on_delete=CASCADE                 | Устройство                  |
| `ip_address`    | GenericIPAddressField | -                                                   | IP-адрес                    |
| `country`       | ForeignKey            | → geodata.GeoCountry, on_delete=SET_NULL, null=True | Страна (определяется по IP) |
| `login_at`      | DateTimeField         | auto_now_add=True                                   | Время входа                 |
| `logout_at`     | DateTimeField         | null=True, blank=True                               | Время выхода                |
| `is_successful` | BooleanField          | default=True                                        | Успешная авторизация        |

**Особенности:**

- Автоматическое определение страны по IP-адресу
- Автоматическое логирование через signals

**Связи:**

- `user` → `main.User` (N:1)
- `device` → `SecurityDevice` (N:1)
- `country` → `geodata.GeoCountry` (N:1)

---

## `SecurityAction`

Типы действий безопасности.

| Поле           | Тип               | Параметры                      | Описание               |
|----------------|-------------------|--------------------------------|------------------------|
| `action_code`  | CharField         | max_length=20, unique=True     | Код действия           |
| `action_name`  | CharField         | max_length=30                  | Название действия      |
| `template`     | CharField         | max_length=250                 | Шаблон уведомления     |
| `action_value` | SmallIntegerField | default=3, choices=[1,2,3,4,5] | Уровень важности (1-5) |

**Уровни важности:**

- 1 — Мусорное
- 2 — Неважное
- 3 — Обычное
- 4 — Важное
- 5 — Критическое

**Связи:**

- `notices` → `SecurityNotice` (1:N)

---

## `SecurityNotice`

Уведомления безопасности для пользователей.

| Поле         | Тип           | Параметры                           | Описание          |
|--------------|---------------|-------------------------------------|-------------------|
| `user`       | ForeignKey    | → main.User, on_delete=CASCADE      | Пользователь      |
| `action`     | ForeignKey    | → SecurityAction, on_delete=CASCADE | Действие          |
| `message`    | TextField     | -                                   | Текст уведомления |
| `is_read`    | BooleanField  | default=False                       | Прочитано         |
| `created_at` | DateTimeField | auto_now_add=True                   | Дата создания     |

**Связи:**

- `user` → `main.User` (N:1)
- `action` → `SecurityAction` (N:1)

---

## Диаграмма связей

```
main.User
  ├── SecurityAuthLog (1:N)
  └── SecurityNotice (1:N)

SecurityDevice
  └── SecurityAuthLog (1:N)

SecurityAction
  └── SecurityNotice (1:N)

geodata.GeoCountry
  └── SecurityAuthLog (1:N)
```

