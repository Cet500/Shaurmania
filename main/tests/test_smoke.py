import time

from django.test import TestCase
from django.urls import reverse
from Shaurmania.settings import TEST_MAX_RESPONSE_TIME


class MainPagesSmokeTest( TestCase ):
	urls_to_test = [
		# название теста, имя маршрута, ожидаемый статус, слово/фраза для проверки
		( 'Главная ',          'index',          200, 'Мания'),
		( 'Каталог',           'catalog',        200, 'Наш каталог шаурмы'),
		( 'Поиск',             'search',         200, 'Поиск' ),
		( 'Логин',             'login',          200, 'Вход' ),
		( 'Регистрация',       'reg',            200, 'Регистрация' ),
		( 'Выход',             'logout',         302, 'Выход' ),
		( 'О нас',             'about',          200, 'О нас'),
		( 'Адрес',             'locations',      200, 'Наши заведения' ),
		( 'Новости',           'news',           200, 'Новости' ),
		( 'Отзывы',            'feedback',       200, 'Легендарные отзывы' ),
		( 'Документы',         'docs',           200, 'Наши официальные документы' ),
		( 'Политика конф.',    'privacy_policy', 200, 'Политика конфиденциальности' ),
		( 'Польз. соглашение', 'user_agreement', 200, 'Пользовательское соглашение' ),
		( 'Согласие',          'user_consent',   200, 'Согласие на обработку персональных данных' ),
		( 'Лицензия',          'license',        200, 'Лицензия на продажу шаурмы' ),
		( 'Приложение 1',      'add_license_1',  200, 'Приложение к лицензии' ),
		( 'Сан. правила',      'san_rules',      200, 'Санитарные правила' ),
		( 'Кодекс',            'codex',          200, 'Кодекс Шаурмиста' ),
		( 'Декрет',            'decree',         200, 'Декрет о шаурмизации' ),
		( 'Акции',             'stocks',         200, 'Акции' ),
	]

	def test_urls_availability_and_content( self ):
		for test_name, route_name, expected_status, word in self.urls_to_test:
			with self.subTest( test = test_name ):
				url = reverse( route_name )

				start_time = time.perf_counter()
				response = self.client.get( url )
				elapsed = time.perf_counter() - start_time

				# Проверяем статус
				self.assertEqual(
					response.status_code,
					expected_status,
					f"{test_name}: expected {expected_status}, got {response.status_code}"
				)

				# Проверяем наличие ключевого слова
				if expected_status == 200 and word:
					self.assertContains(
						response,
						word,
						msg_prefix = f"{test_name}: not found word «{word}»"
					)

				# Проверяем скорость ответа
				self.assertLessEqual(
					elapsed,
					TEST_MAX_RESPONSE_TIME,
					f"{test_name}: too slowly answer ({elapsed:.3f}s)"
				)
