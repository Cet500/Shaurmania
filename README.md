# Шаурмания

Сайт по продаже Шаурмы с доставкой.

На данном этапе мы работаем с базой данных и доработками страниц.

## Сохранение данных

python -Xutf8 manage.py dumpdata main.Review -o main/fixtures/reviews.json
python -Xutf8 manage.py dumpdata main.Shaurma -o main/fixtures/shaurma.json
