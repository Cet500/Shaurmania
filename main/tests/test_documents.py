from django.test import TestCase
from django.urls import reverse


class DocumentsPagesTest( TestCase ):
	"""Специальные тесты для страниц документов с проверкой структуры и содержимого"""

	def test_docs_list_page_structure( self ):
		"""Проверка структуры главной страницы документов"""
		resp = self.client.get( reverse( 'docs' ) )
		self.assertEqual( resp.status_code, 200 )
		content = resp.content.decode( 'utf-8' )

		# Проверка наличия основных блоков документов
		self.assertIn( 'Наши официальные документы', content )
		self.assertIn( 'block-docs', content )
		self.assertIn( 'btn_catalog', content )

		# Проверка наличия ссылок на документы в отрендеренном HTML
		self.assertIn( 'href="/docs/license"', content )
		self.assertIn( 'href="/docs/decree"', content )
		self.assertIn( 'href="/docs/codex"', content )
		self.assertIn( 'href="/docs/san_rules"', content )
		self.assertIn( 'href="/docs/privacy_policy"', content )
		self.assertIn( 'href="/docs/user_agreement"', content )
		self.assertIn( 'href="/docs/user_consent"', content )

	def test_privacy_policy_structure( self ):
		"""Проверка структуры политики конфиденциальности"""
		resp = self.client.get( reverse( 'privacy_policy' ) )
		self.assertEqual( resp.status_code, 200 )
		content = resp.content.decode( 'utf-8' )

		# Проверка заголовка
		self.assertIn( 'Политика конфиденциальности', content )

		# Проверка наличия документального блока
		self.assertIn( 'block-document', content )

		# Проверка ключевых разделов
		self.assertIn( 'Общие положения', content )
		self.assertIn( 'Состав персональных данных', content )
		self.assertIn( 'Цели обработки персональных данных', content )
		self.assertIn( 'Условия обработки и передачи данных', content )
		self.assertIn( 'Файлы cookie', content )

		# Проверка наличия структурированных списков
		self.assertIn( '<ul>', content )
		self.assertIn( '152-ФЗ', content )

	def test_user_agreement_structure( self ):
		"""Проверка структуры пользовательского соглашения"""
		resp = self.client.get( reverse( 'user_agreement' ) )
		self.assertEqual( resp.status_code, 200 )
		content = resp.content.decode( 'utf-8' )

		# Проверка заголовка
		self.assertIn( 'Пользовательское соглашение', content )

		# Проверка наличия документального блока
		self.assertIn( 'block-document', content )

		# Проверка ключевых разделов
		self.assertIn( 'Статус Соглашения', content )
		self.assertIn( 'Интеллектуальная собственность', content )
		self.assertIn( 'Условия использования сервисов', content )
		self.assertIn( 'Отказ от ответственности', content )
		self.assertIn( 'Регистрация и учётная запись', content )
		self.assertIn( 'Разрешение споров', content )

		# Проверка важного предупреждения
		self.assertIn( 'КАК ЕСТЬ', content )
		self.assertIn( 'публичной офертой', content )

	def test_user_consent_structure( self ):
		"""Проверка структуры формы согласия на обработку данных"""
		resp = self.client.get( reverse( 'user_consent' ) )
		self.assertEqual( resp.status_code, 200 )
		content = resp.content.decode( 'utf-8' )

		# Проверка заголовка
		self.assertIn( 'Согласие на обработку персональных данных', content )

		# Проверка наличия документального блока
		self.assertIn( 'block-document', content )

		# Проверка ключевых разделов
		self.assertIn( 'Перечень обрабатываемых данных', content )
		self.assertIn( 'Цели обработки', content )
		self.assertIn( 'Способы обработки', content )
		self.assertIn( 'Срок действия согласия', content )

		# Проверка наличия ссылок на связанные документы в отрендеренном HTML
		self.assertIn( 'href="/docs/user_agreement"', content )
		self.assertIn( 'href="/docs/privacy_policy"', content )

	def test_license_structure( self ):
		"""Проверка структуры лицензии"""
		resp = self.client.get( reverse( 'license' ) )
		self.assertEqual( resp.status_code, 200 )
		content = resp.content.decode( 'utf-8' )

		self.assertIn( 'Лицензия на продажу шаурмы', content )
		self.assertIn( 'block-document', content )
		self.assertIn( 'Общие положения', content )
		self.assertIn( 'Льва Троцкого', content )

	def test_decree_structure( self ):
		"""Проверка структуры декрета"""
		resp = self.client.get( reverse( 'decree' ) )
		self.assertEqual( resp.status_code, 200 )
		content = resp.content.decode( 'utf-8' )

		self.assertIn( 'Декрет', content )
		self.assertIn( 'block-document', content )
		self.assertIn( 'ВЦИК', content )

	def test_codex_structure( self ):
		"""Проверка структуры кодекса"""
		resp = self.client.get( reverse( 'codex' ) )
		self.assertEqual( resp.status_code, 200 )
		content = resp.content.decode( 'utf-8' )

		self.assertIn( 'Кодекс Шаурмиста', content )
		self.assertIn( 'block-document', content )
		self.assertIn( 'Догма', content )

	def test_san_rules_structure( self ):
		"""Проверка структуры санитарных правил"""
		resp = self.client.get( reverse( 'san_rules' ) )
		self.assertEqual( resp.status_code, 200 )
		content = resp.content.decode( 'utf-8' )

		self.assertIn( 'Санитарные правила', content )
		self.assertIn( 'САНПИН', content )
		self.assertIn( 'block-document', content )

	def test_add_license_1_structure( self ):
		"""Проверка структуры приложения к лицензии"""
		resp = self.client.get( reverse( 'add_license_1' ) )
		self.assertEqual( resp.status_code, 200 )
		content = resp.content.decode( 'utf-8' )

		self.assertIn( 'Приложение', content )
		self.assertIn( 'block-document', content )
		self.assertIn( 'невозможных', content )

	def test_all_documents_have_document_block( self ):
		"""Проверка, что все документы имеют блок document"""
		document_urls = [
			'privacy_policy', 'user_agreement', 'user_consent',
			'license', 'add_license_1', 'san_rules', 'codex', 'decree'
		]

		for url_name in document_urls:
			with self.subTest( url_name = url_name ):
				resp = self.client.get( reverse( url_name ) )
				self.assertEqual( resp.status_code, 200 )
				content = resp.content.decode( 'utf-8' )
				# Проверка наличия блока документа (старый или новый стиль)
				self.assertTrue(
					'block-document' in content or 'block-document-modern' in content,
					f"Document {url_name} should contain block-document or block-document-modern"
				)

	def test_all_documents_have_title( self ):
		"""Проверка, что все документы имеют заголовок h2"""
		document_urls = [
			'privacy_policy', 'user_agreement', 'user_consent',
			'license', 'add_license_1', 'san_rules', 'codex', 'decree'
		]

		for url_name in document_urls:
			with self.subTest( url_name = url_name ):
				resp = self.client.get( reverse( url_name ) )
				self.assertEqual( resp.status_code, 200 )
				content = resp.content.decode( 'utf-8' )
				# Проверка наличия заголовка
				self.assertIn( '<h2', content, f"Document {url_name} should have h2 title" )

	def test_documents_content_structure( self ):
		"""Проверка правильной структуры контента документов"""
		document_tests = {
			'privacy_policy': ['<p>', '<b>', '<ul>', '<li>'],
			'user_agreement': ['<p>', '<b>', '<ul>', '<li>'],
			'user_consent'  : ['<p>', '<b>', '<ul>', '<li>'],
			'license'       : ['<p>', '<b>', '<ul>', '<li>'],
			'decree'        : ['<p>', '<b>', '<ul>'],
			'codex'         : ['<p>', '<b>'],
			'san_rules'     : ['<p>', '<b>'],
			'add_license_1' : ['<p>', '<b>', '<ul>', '<li>'],
		}

		for url_name, required_tags in document_tests.items():
			with self.subTest( url_name = url_name ):
				resp = self.client.get( reverse( url_name ) )
				self.assertEqual( resp.status_code, 200 )
				content = resp.content.decode( 'utf-8' )

				for tag in required_tags:
					self.assertIn( tag, content,f"Document {url_name} should contain {tag} tag" )
