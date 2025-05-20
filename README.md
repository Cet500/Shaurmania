# ШаурМания

Сайт по продаже Шаурмы с доставкой.

На данном этапе мы работаем с базой данных и доработками страниц.

> Версия данных: 4

## Сохранение данных

	python -Xutf8 manage.py dumpdata main.ShaurmaCategory -o main/fixtures/shaurma_categories.json
	python -Xutf8 manage.py dumpdata main.Shaurma -o main/fixtures/shaurma.json
    python -Xutf8 manage.py dumpdata main.Review -o main/fixtures/reviews.json
    python -Xutf8 manage.py dumpdata main.Location -o main/fixtures/locations.json
    python -Xutf8 manage.py dumpdata main.Achievement -o main/fixtures/achievements.json
    python -Xutf8 manage.py dumpdata main.Stock -o main/fixtures/stocks.json
	python -Xutf8 manage.py dumpdata main.Promocode -o main/fixtures/promocodes.json

## Загрузка данных

	python manage.py loaddata shaurma_categories.json
    python manage.py loaddata shaurma.json
    python manage.py loaddata reviews.json
    python manage.py loaddata locations.json
    python manage.py loaddata achievements.json
    python manage.py loaddata stocks.json
	python manage.py loaddata promocodes.json
